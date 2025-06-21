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


def get_inventory_items(skip: int = 0, limit: int = 100, search: Optional[str] = None,
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


def get_inventory_item_by_id(item_id: int):
    """Get a single inventory item with all details"""
    item = db.execute_query("""
        SELECT i.*, c.name_en as category_name_en, c.name_mi as category_name_mi,
               l.name_en as location_name_en, l.name_mi as location_name_mi,
               s.name as supplier_name, s.contact_person as supplier_contact,
               s.email as supplier_email, s.phone as supplier_phone,
               (CASE WHEN i.expiry_date IS NOT NULL AND date(i.expiry_date) <= date('now', '+30 days')
                     THEN 1 ELSE 0 END) as is_expiring_soon,
               (julianday(i.expiry_date) - julianday('now')) as days_until_expiry
        FROM inventory_items i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN locations l ON i.location_id = l.id
        LEFT JOIN suppliers s ON i.supplier_id = s.id
        WHERE i.id = ?
    """, (item_id,), fetch_one=True)
    
    if not item:
        return None
    
    # Get variants
    variants = db.execute_query("""
        SELECT * FROM product_variants 
        WHERE parent_item_id = ? AND is_active = 1
        ORDER BY variant_name, variant_value
    """, (item_id,), fetch_all=True)
    
    # Get recent stock movements
    movements = db.execute_query("""
        SELECT sm.*, u.first_name || ' ' || u.last_name as user_name,
               fl.name_en as from_location, tl.name_en as to_location
        FROM stock_movements sm
        JOIN users u ON sm.user_id = u.id
        LEFT JOIN locations fl ON sm.from_location_id = fl.id
        LEFT JOIN locations tl ON sm.to_location_id = tl.id
        WHERE sm.item_id = ?
        ORDER BY sm.created_at DESC
        LIMIT 10
    """, (item_id,), fetch_all=True)
    
    # Get maintenance records
    maintenance = db.execute_query("""
        SELECT mr.*, u.first_name || ' ' || u.last_name as created_by_name
        FROM maintenance_records mr
        LEFT JOIN users u ON mr.created_by = u.id
        WHERE mr.item_id = ?
        ORDER BY mr.created_at DESC
        LIMIT 5
    """, (item_id,), fetch_all=True)
    
    # Get current bookings
    bookings = db.execute_query("""
        SELECT b.*, u.first_name || ' ' || u.last_name as user_name
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        WHERE b.item_id = ? AND b.status IN ('Approved', 'Active')
        ORDER BY b.start_date
    """, (item_id,), fetch_all=True)
    
    return {
        **item,
        "variants": variants,
        "recent_movements": movements,
        "maintenance_records": maintenance,
        "current_bookings": bookings
    }


def get_inventory_item_by_barcode(barcode: str):
    """Get inventory item by barcode or SKU"""
    return db.execute_query("""
        SELECT i.*, c.name_en as category_name_en, c.name_mi as category_name_mi,
               l.name_en as location_name_en, l.name_mi as location_name_mi,
               s.name as supplier_name
        FROM inventory_items i
        LEFT JOIN categories c ON i.category_id = c.id
        LEFT JOIN locations l ON i.location_id = l.id
        LEFT JOIN suppliers s ON i.supplier_id = s.id
        WHERE (i.barcode = ? OR i.sku = ?) AND i.is_active = 1
    """, (barcode, barcode), fetch_one=True)


def create_inventory_item(item: InventoryItemCreate, user_id: int):
    """Create a new inventory item with comprehensive features"""
    # Convert tags to JSON string
    tags_json = json.dumps(item.tags) if item.tags else None
    
    # Generate SKU if not provided
    sku = item.sku
    if not sku:
        # Generate SKU based on category and sequence
        category_code = "GEN"
        if item.category_id:
            category = db.execute_query(
                "SELECT name_en FROM categories WHERE id = ?",
                (item.category_id,), fetch_one=True
            )
            if category:
                category_code = category['name_en'][:3].upper()
        
        # Get next sequence number
        last_item = db.execute_query(
            "SELECT MAX(id) as max_id FROM inventory_items", fetch_one=True
        )
        next_id = (last_item['max_id'] or 0) + 1
        sku = f"{category_code}-{next_id:04d}"
    
    # Create inventory item
    item_id = db.execute_query(
        """INSERT INTO inventory_items 
           (name_en, name_mi, description_en, description_mi, category_id,
            barcode, sku, serial_number, quantity, reserved_quantity, unit, 
            location_id, condition_status, purchase_date, purchase_cost, 
            supplier_id, warranty_expiry, expiry_date, reorder_level, 
            max_stock_level, is_active, is_loanable, loan_duration_days, 
            tags, notes, weight, dimensions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (item.name_en, item.name_mi, item.description_en, item.description_mi,
         item.category_id, item.barcode, sku, item.serial_number, 
         item.quantity, item.reserved_quantity, item.unit, item.location_id, 
         item.condition_status, item.purchase_date, item.purchase_cost, 
         item.supplier_id, item.warranty_expiry, item.expiry_date, 
         item.reorder_level, item.max_stock_level, item.is_active, 
         item.is_loanable, item.loan_duration_days, tags_json, item.notes,
         item.weight, item.dimensions)
    )
    
    # Create initial stock movement if quantity > 0
    if item.quantity > 0:
        db.create_stock_movement(
            item_id=item_id,
            movement_type=MovementType.IN,
            quantity=item.quantity,
            user_id=user_id,
            to_location_id=item.location_id,
            reference_type='initial_stock',
            unit_cost=item.purchase_cost,
            total_cost=item.purchase_cost * item.quantity if item.purchase_cost else None,
            reason='Initial stock entry',
            notes='Item created with initial stock'
        )
    
    # Update inventory valuation
    if item.purchase_cost:
        db.update_inventory_valuation(item_id, 'AVERAGE')
    
    # Log audit
    db.log_audit(user_id, "CREATE", "inventory_items", item_id, {}, item.dict())
    
    # Check for low stock alert
    check_and_create_stock_alerts(item_id)
    
    # Get created item with all details
    return get_inventory_item_by_id(item_id)


def update_inventory_item(item_id: int, item_update: InventoryItemUpdate, user_id: int):
    """Update an inventory item"""
    # Get current item
    current_item = db.execute_query(
        "SELECT * FROM inventory_items WHERE id = ?",
        (item_id,), fetch_one=True
    )
    
    if not current_item:
        return None
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    for field, value in item_update.dict(exclude_unset=True).items():
        if field == 'tags' and value is not None:
            update_fields.append(f"{field} = ?")
            params.append(json.dumps(value))
        else:
            update_fields.append(f"{field} = ?")
            params.append(value)
    
    if not update_fields:
        return get_inventory_item_by_id(item_id)
    
    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    params.append(item_id)
    
    # Execute update
    db.execute_query(
        f"UPDATE inventory_items SET {', '.join(update_fields)} WHERE id = ?",
        tuple(params)
    )
    
    # Handle quantity changes
    if hasattr(item_update, 'quantity') and item_update.quantity is not None:
        quantity_diff = item_update.quantity - current_item['quantity']
        if quantity_diff != 0:
            movement_type = MovementType.IN if quantity_diff > 0 else MovementType.OUT
            db.create_stock_movement(
                item_id=item_id,
                movement_type=MovementType.ADJUSTMENT,
                quantity=quantity_diff,
                user_id=user_id,
                reference_type='manual_adjustment',
                reason=f'Manual quantity adjustment: {current_item["quantity"]} → {item_update.quantity}',
                notes='Quantity updated via item edit'
            )
    
    # Log audit
    db.log_audit(user_id, "UPDATE", "inventory_items", item_id, 
                 current_item, item_update.dict(exclude_unset=True))
    
    # Check for alerts
    check_and_create_stock_alerts(item_id)
    
    return get_inventory_item_by_id(item_id)


def delete_inventory_item(item_id: int, user_id: int):
    """Soft delete an inventory item"""
    # Check if item has active bookings
    active_bookings = db.execute_query("""
        SELECT COUNT(*) as count FROM bookings 
        WHERE item_id = ? AND status IN ('Approved', 'Active')
    """, (item_id,), fetch_one=True)
    
    if active_bookings['count'] > 0:
        return {"error": "Cannot delete item with active bookings"}
    
    # Soft delete (mark as inactive)
    db.execute_query(
        "UPDATE inventory_items SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (item_id,)
    )
    
    # Log audit
    db.log_audit(user_id, "DELETE", "inventory_items", item_id, {}, {"is_active": False})
    
    return {"message": "Item successfully deactivated"}


def create_stock_movement(movement: StockMovementCreate, user_id: int):
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
    
    # Check for alerts
    check_and_create_stock_alerts(movement.item_id)
    
    return {"movement_id": movement_id, "message": "Stock movement created successfully"}


def get_stock_movements(item_id: Optional[int] = None, days_back: int = 90, 
                       movement_type: Optional[str] = None, limit: int = 100):
    """Get stock movement history with filtering"""
    query = """
        SELECT sm.*, i.name_en as item_name, u.first_name || ' ' || u.last_name as user_name,
               fl.name_en as from_location, tl.name_en as to_location
        FROM stock_movements sm
        JOIN inventory_items i ON sm.item_id = i.id
        JOIN users u ON sm.user_id = u.id
        LEFT JOIN locations fl ON sm.from_location_id = fl.id
        LEFT JOIN locations tl ON sm.to_location_id = tl.id
        WHERE date(sm.created_at) >= date('now', '-' || ? || ' days')
    """
    
    params = [days_back]
    
    if item_id:
        query += " AND sm.item_id = ?"
        params.append(item_id)
    
    if movement_type:
        query += " AND sm.movement_type = ?"
        params.append(movement_type)
    
    query += " ORDER BY sm.created_at DESC LIMIT ?"
    params.append(limit)
    
    return db.execute_query(query, tuple(params), fetch_all=True)


def create_product_variant(variant: ProductVariantCreate, user_id: int):
    """Create a product variant"""
    # Validate parent item exists
    parent_item = db.execute_query(
        "SELECT id FROM inventory_items WHERE id = ? AND is_active = 1",
        (variant.parent_item_id,), fetch_one=True
    )
    
    if not parent_item:
        return {"error": "Parent item not found or inactive"}
    
    # Create variant
    variant_id = db.execute_query(
        """INSERT INTO product_variants 
           (parent_item_id, variant_name, variant_value, sku, barcode, 
            quantity, additional_cost, is_active)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (variant.parent_item_id, variant.variant_name, variant.variant_value,
         variant.sku, variant.barcode, variant.quantity, variant.additional_cost,
         variant.is_active)
    )
    
    # Log audit
    db.log_audit(user_id, "CREATE", "product_variants", variant_id, {}, variant.dict())
    
    # Get created variant
    created_variant = db.execute_query(
        "SELECT * FROM product_variants WHERE id = ?",
        (variant_id,), fetch_one=True
    )
    
    return created_variant


def get_low_stock_items():
    """Get items below reorder level"""
    return db.get_low_stock_items('reorder_level')


def get_out_of_stock_items():
    """Get items that are out of stock"""
    return db.get_low_stock_items('out_of_stock')


def get_expiring_items(days_ahead: int = 30):
    """Get items expiring within specified days"""
    return db.get_expiring_items(days_ahead)


def check_and_create_stock_alerts(item_id: int):
    """Check inventory levels and create alerts if needed"""
    item = db.execute_query(
        "SELECT * FROM inventory_items WHERE id = ?",
        (item_id,), fetch_one=True
    )
    
    if not item:
        return
    
    alerts_to_create = []
    
    # Check low stock
    if item['reorder_level'] > 0 and item['quantity'] <= item['reorder_level']:
        if item['quantity'] == 0:
            alerts_to_create.append({
                'alert_type': 'OUT_OF_STOCK',
                'threshold_value': 0,
                'current_value': item['quantity'],
                'message': f"Item '{item['name_en']}' is out of stock"
            })
        else:
            alerts_to_create.append({
                'alert_type': 'LOW_STOCK',
                'threshold_value': item['reorder_level'],
                'current_value': item['quantity'],
                'message': f"Item '{item['name_en']}' is below reorder level ({item['quantity']} <= {item['reorder_level']})"
            })
    
    # Check overstock
    if item['max_stock_level'] > 0 and item['quantity'] > item['max_stock_level']:
        alerts_to_create.append({
            'alert_type': 'OVERSTOCK',
            'threshold_value': item['max_stock_level'],
            'current_value': item['quantity'],
            'message': f"Item '{item['name_en']}' exceeds maximum stock level ({item['quantity']} > {item['max_stock_level']})"
        })
    
    # Check expiry
    if item['expiry_date']:
        days_until_expiry = db.execute_query("""
            SELECT (julianday(?) - julianday('now')) as days
        """, (item['expiry_date'],), fetch_one=True)['days']
        
        if days_until_expiry <= 30:  # 30 days warning
            alerts_to_create.append({
                'alert_type': 'EXPIRY_WARNING',
                'threshold_value': 30,
                'current_value': days_until_expiry,
                'message': f"Item '{item['name_en']}' expires in {int(days_until_expiry)} days"
            })
    
    # Create alerts
    for alert_data in alerts_to_create:
        # Check if similar alert already exists and is active
        existing = db.execute_query("""
            SELECT id FROM stock_alerts 
            WHERE item_id = ? AND alert_type = ? AND is_active = 1
        """, (item_id, alert_data['alert_type']), fetch_one=True)
        
        if not existing:
            db.execute_query("""
                INSERT INTO stock_alerts 
                (item_id, alert_type, threshold_value, current_value, message, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (item_id, alert_data['alert_type'], alert_data['threshold_value'],
                  alert_data['current_value'], alert_data['message']))


def get_active_stock_alerts():
    """Get all active stock alerts"""
    return db.execute_query("""
        SELECT sa.*, i.name_en as item_name, i.sku, l.name_en as location_name
        FROM stock_alerts sa
        JOIN inventory_items i ON sa.item_id = i.id
        LEFT JOIN locations l ON i.location_id = l.id
        WHERE sa.is_active = 1
        ORDER BY sa.created_at DESC
    """, fetch_all=True)


def acknowledge_stock_alert(alert_id: int, user_id: int):
    """Acknowledge a stock alert"""
    db.execute_query("""
        UPDATE stock_alerts 
        SET is_active = 0, acknowledged_by = ?, acknowledged_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (user_id, alert_id))
    
    return {"message": "Alert acknowledged successfully"}


def bulk_stock_adjustment(adjustments: List[Dict], reason: str, notes: str, user_id: int):
    """Perform bulk stock adjustments"""
    results = []
    
    for adjustment in adjustments:
        item_id = adjustment.get('item_id')
        new_quantity = adjustment.get('new_quantity')
        
        # Get current quantity
        current = db.execute_query(
            "SELECT quantity FROM inventory_items WHERE id = ?",
            (item_id,), fetch_one=True
        )
        
        if not current:
            results.append({"item_id": item_id, "error": "Item not found"})
            continue
        
        quantity_diff = new_quantity - current['quantity']
        
        if quantity_diff != 0:
            # Create stock movement
            db.create_stock_movement(
                item_id=item_id,
                movement_type=MovementType.ADJUSTMENT,
                quantity=quantity_diff,
                user_id=user_id,
                reference_type='bulk_adjustment',
                reason=reason,
                notes=notes
            )
            
            results.append({
                "item_id": item_id, 
                "old_quantity": current['quantity'],
                "new_quantity": new_quantity,
                "adjustment": quantity_diff,
                "success": True
            })
            
            # Check alerts
            check_and_create_stock_alerts(item_id)
        else:
            results.append({
                "item_id": item_id,
                "message": "No change required",
                "success": True
            })
    
    return {"results": results, "total_processed": len(adjustments)}


def get_inventory_summary():
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
    
    summary['low_stock_items'] = len(get_low_stock_items())
    summary['out_of_stock_items'] = len(get_out_of_stock_items())
    summary['expiring_items'] = len(get_expiring_items())
    
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
    
    # By condition
    summary['by_condition'] = db.execute_query("""
        SELECT condition_status, COUNT(*) as count
        FROM inventory_items
        WHERE is_active = 1
        GROUP BY condition_status
        ORDER BY count DESC
    """, fetch_all=True)
    
    return summary