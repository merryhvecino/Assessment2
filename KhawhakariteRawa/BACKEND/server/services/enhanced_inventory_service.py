#!/usr/bin/env python3
"""
Enhanced inventory service for Kaiwhakarite Rawa
Supports comprehensive inventory management features
"""

import json
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from ..database import db
from ..models import (
    InventoryItemCreate, InventoryItemUpdate, StockMovementCreate,
    ProductVariantCreate, MovementType, ConditionStatus
)


def get_inventory_items_enhanced(skip: int = 0, limit: int = 100, search: Optional[str] = None,
                                category_id: Optional[int] = None, location_id: Optional[int] = None,
                                condition: Optional[str] = None, is_active: Optional[bool] = None,
                                low_stock_only: bool = False, expiring_only: bool = False,
                                expiry_days: int = 30):
    """Get inventory items with comprehensive filtering and pagination"""
    # Build query
    query = """
        SELECT i.*, c.name_en as category_name_en, c.name_mi as category_name_mi,
            l.name_en as location_name_en, l.name_mi as location_name_mi,
            s.name as supplier_name,
            (CASE WHEN i.expiry_date IS NOT NULL AND date(i.expiry_date) <= date('now', '+' || ? || ' days')
                    THEN 1 ELSE 0 END) as is_expiring_soon,
            (julianday(i.expiry_date) - julianday('now')) as days_until_expiry
        FROM inventory_items i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN locations l ON i.location_id = l.id
        LEFT JOIN suppliers s ON i.supplier_id = s.id
        WHERE 1=1
    """
    
    params = [expiry_days]
    
    if search:
        search_param = f"%{search}%"
        query += """ AND (i.name_en LIKE ? OR i.name_mi LIKE ? 
                        OR i.description_en LIKE ? OR i.barcode LIKE ? OR i.sku LIKE ?)"""
        params.extend([search_param, search_param, search_param, search_param, search_param])
    
    if category_id:
        query += " AND i.category_id = ?"
        params.append(category_id)
    
    if location_id:
        query += " AND i.location_id = ?"
        params.append(location_id)
    
    if condition:
        query += " AND i.condition_status = ?"
        params.append(condition)
    
    if is_active is not None:
        query += " AND i.is_active = ?"
        params.append(1 if is_active else 0)
    
    if low_stock_only:
        query += " AND i.quantity <= i.reorder_level AND i.reorder_level > 0"
    
    if expiring_only:
        query += " AND i.expiry_date IS NOT NULL AND date(i.expiry_date) <= date('now', '+' || ? || ' days')"
        params.append(expiry_days)
    
    query += " ORDER BY i.name_en LIMIT ? OFFSET ?"
    params.extend([limit, skip])
    
    items = db.execute_query(query, tuple(params), fetch_all=True)
    
    # Get total count for pagination
    count_query = "SELECT COUNT(*) FROM inventory_items i WHERE 1=1"
    count_params = []
    
    if search:
        count_query += """ AND (i.name_en LIKE ? OR i.name_mi LIKE ? 
                            OR i.description_en LIKE ? OR i.barcode LIKE ? OR i.sku LIKE ?)"""
        count_params.extend([search_param, search_param, search_param, search_param, search_param])
    
    if category_id:
        count_query += " AND i.category_id = ?"
        count_params.append(category_id)
    
    if location_id:
        count_query += " AND i.location_id = ?"
        count_params.append(location_id)
    
    if condition:
        count_query += " AND i.condition_status = ?"
        count_params.append(condition)
    
    if is_active is not None:
        count_query += " AND i.is_active = ?"
        count_params.append(1 if is_active else 0)
    
    if low_stock_only:
        count_query += " AND i.quantity <= i.reorder_level AND i.reorder_level > 0"
    
    if expiring_only:
        count_query += " AND i.expiry_date IS NOT NULL AND date(i.expiry_date) <= date('now', '+' || ? || ' days')"
        count_params.append(expiry_days)
    
    total = db.execute_query(count_query, tuple(count_params), fetch_one=True)[0]
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "filters": {
            "search": search,
            "category_id": category_id,
            "location_id": location_id,
            "condition": condition,
            "is_active": is_active,
            "low_stock_only": low_stock_only,
            "expiring_only": expiring_only
        }
    }


def create_stock_movement_enhanced(movement: StockMovementCreate, user_id: int):
    """Create a stock movement and update inventory"""
    # Validate item exists
    item = db.execute_query(
        "SELECT * FROM inventory_items WHERE id = ? AND is_active = 1",
        (movement.item_id,), fetch_one=True
    )
    
    if not item:
        return {"error": "Item not found or inactive"}
    
    # Validate sufficient stock for OUT movements
    if movement.movement_type in [MovementType.OUT, MovementType.TRANSFER]:
        if item['quantity'] < movement.quantity:
            return {"error": f"Insufficient stock. Available: {item['quantity']}, Requested: {movement.quantity}"}
    
    # Create movement
    movement_id = db.create_stock_movement(
        item_id=movement.item_id,
        movement_type=movement.movement_type,
        quantity=movement.quantity,
        user_id=user_id,
        from_location_id=movement.from_location_id,
        to_location_id=movement.to_location_id,
        reference_id=movement.reference_id,
        reference_type=movement.reference_type,
        unit_cost=movement.unit_cost,
        total_cost=movement.total_cost,
        reason=movement.reason,
        notes=movement.notes
    )
    
    # Update location if transfer
    if movement.movement_type == MovementType.TRANSFER and movement.to_location_id:
        db.execute_query(
            "UPDATE inventory_items SET location_id = ? WHERE id = ?",
            (movement.to_location_id, movement.item_id)
        )
    
    # Update valuation if cost provided
    if movement.unit_cost and movement.movement_type == MovementType.IN:
        db.update_inventory_valuation(movement.item_id, 'AVERAGE')
    
    return {"movement_id": movement_id, "message": "Stock movement created successfully"}


def get_inventory_summary_enhanced():
    """Get comprehensive inventory summary"""
    summary = {}
    
    # Basic counts
    summary['total_items'] = db.execute_query(
        "SELECT COUNT(*) as count FROM inventory_items WHERE is_active = 1",
        fetch_one=True
    )['count']
    
    summary['total_value'] = db.execute_query(
        "SELECT SUM(current_value) as total FROM inventory_items WHERE is_active = 1",
        fetch_one=True
    )['total'] or 0
    
    summary['low_stock_items'] = len(db.get_low_stock_items('reorder_level'))
    summary['out_of_stock_items'] = len(db.get_low_stock_items('out_of_stock'))
    summary['expiring_items'] = len(db.get_expiring_items())
    
    # By category
    summary['by_category'] = db.execute_query("""
        SELECT c.name_en as category, COUNT(i.id) as count, 
            SUM(i.current_value) as total_value
        FROM inventory_items i
        LEFT JOIN categories c ON i.category_id = c.id
        WHERE i.is_active = 1
        GROUP BY c.id, c.name_en
        ORDER BY count DESC
    """, fetch_all=True)
    
    # By location
    summary['by_location'] = db.execute_query("""
        SELECT l.name_en as location, COUNT(i.id) as count,
            SUM(i.current_value) as total_value
        FROM inventory_items i
        LEFT JOIN locations l ON i.location_id = l.id
        WHERE i.is_active = 1
        GROUP BY l.id, l.name_en
        ORDER BY count DESC
    """, fetch_all=True)
    
    return summary 