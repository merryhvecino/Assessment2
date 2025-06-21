#!/usr/bin/env python3
"""
Enhanced inventory routes for Kaiwhakarite Rawa
Supports comprehensive inventory management features
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from datetime import date
from ..auth import get_current_user
from ..models import (
    InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse,
    StockMovementCreate, StockMovementResponse, ProductVariantCreate,
    ProductVariantResponse, MovementType, ConditionStatus
)
from ..services.enhanced_inventory_service import (
    get_inventory_items_enhanced, create_stock_movement_enhanced,
    get_inventory_summary_enhanced
)
from ..database import db

router = APIRouter(prefix="/api/inventory", tags=["Enhanced Inventory"])


@router.get("/items/enhanced", response_model=dict)
async def get_inventory_items_enhanced_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    condition: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(True),
    low_stock_only: bool = Query(False),
    expiring_only: bool = Query(False),
    expiry_days: int = Query(30, ge=1, le=365),
    current_user: dict = Depends(get_current_user)
):
    """Get inventory items with enhanced filtering and pagination"""
    try:
        result = get_inventory_items_enhanced(
            skip=skip,
            limit=limit,
            search=search,
            category_id=category_id,
            location_id=location_id,
            condition=condition,
            is_active=is_active,
            low_stock_only=low_stock_only,
            expiring_only=expiring_only,
            expiry_days=expiry_days
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items/{item_id}/details")
async def get_inventory_item_details(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed inventory item information including variants, movements, and maintenance"""
    try:
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
            raise HTTPException(status_code=404, detail="Item not found")
        
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
            LIMIT 20
        """, (item_id,), fetch_all=True)
        
        # Get maintenance records
        maintenance = db.execute_query("""
            SELECT mr.*, u.first_name || ' ' || u.last_name as created_by_name
            FROM maintenance_records mr
            LEFT JOIN users u ON mr.created_by = u.id
            WHERE mr.item_id = ?
            ORDER BY mr.created_at DESC
            LIMIT 10
        """, (item_id,), fetch_all=True)
        
        # Get current bookings
        bookings = db.execute_query("""
            SELECT b.*, u.first_name || ' ' || u.last_name as user_name
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            WHERE b.item_id = ? AND b.status IN ('Approved', 'Active')
            ORDER BY b.start_date
        """, (item_id,), fetch_all=True)
        
        # Get stock alerts (commented out as stock_alerts table may not exist)
        alerts = []
        # alerts = db.execute_query("""
        #     SELECT * FROM stock_alerts 
        #     WHERE item_id = ? AND is_active = 1
        #     ORDER BY created_at DESC
        # """, (item_id,), fetch_all=True)
        
        return {
            **item,
            "variants": variants,
            "recent_movements": movements,
            "maintenance_records": maintenance,
            "current_bookings": bookings,
            "active_alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/movements", response_model=dict)
async def create_stock_movement(
    movement: StockMovementCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a stock movement"""
    try:
        result = create_stock_movement_enhanced(movement, current_user['id'])
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/movements")
async def get_stock_movements(
    item_id: Optional[int] = Query(None),
    movement_type: Optional[str] = Query(None),
    days_back: int = Query(90, ge=1, le=365),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user)
):
    """Get stock movement history with filtering"""
    try:
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
        
        movements = db.execute_query(query, tuple(params), fetch_all=True)
        return {"movements": movements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/variants", response_model=ProductVariantResponse)
async def create_product_variant(
    variant: ProductVariantCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a product variant"""
    try:
        # Validate parent item exists
        parent_item = db.execute_query(
            "SELECT id FROM inventory_items WHERE id = ?",
            (variant.parent_item_id,), fetch_one=True
        )
        
        if not parent_item:
            raise HTTPException(status_code=404, detail="Parent item not found or inactive")
        
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
        db.log_audit(current_user['id'], "CREATE", "product_variants", variant_id, {}, variant.dict())
        
        # Get created variant
        created_variant = db.execute_query(
            "SELECT * FROM product_variants WHERE id = ?",
            (variant_id,), fetch_one=True
        )
        
        return created_variant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_stock_alerts(
    item_id: Optional[int] = Query(None),
    alert_type: Optional[str] = Query(None),
    is_active: bool = Query(True),
    current_user: dict = Depends(get_current_user)
):
    """Get stock alerts"""
    try:
        query = """
            SELECT sa.*, i.name_en as item_name, i.sku, l.name_en as location_name,
                   u.first_name || ' ' || u.last_name as acknowledged_by_name
            FROM stock_alerts sa
            JOIN inventory_items i ON sa.item_id = i.id
            LEFT JOIN locations l ON i.location_id = l.id
            LEFT JOIN users u ON sa.acknowledged_by = u.id
            WHERE sa.is_active = ?
        """
        
        params = [1 if is_active else 0]
        
        if item_id:
            query += " AND sa.item_id = ?"
            params.append(item_id)
        
        if alert_type:
            query += " AND sa.alert_type = ?"
            params.append(alert_type)
        
        query += " ORDER BY sa.created_at DESC"
        
        alerts = db.execute_query(query, tuple(params), fetch_all=True)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_stock_alert(
    alert_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Acknowledge a stock alert"""
    try:
        alert = db.execute_query(
            "SELECT * FROM stock_alerts WHERE id = ?",
            (alert_id,), fetch_one=True
        )
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        db.execute_query("""
            UPDATE stock_alerts 
            SET is_active = 0, acknowledged_by = ?, acknowledged_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (current_user['id'], alert_id))
        
        return {"message": "Alert acknowledged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/low-stock")
async def get_low_stock_items(
    current_user: dict = Depends(get_current_user)
):
    """Get items below reorder level"""
    try:
        items = db.get_low_stock_items('reorder_level')
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/out-of-stock")
async def get_out_of_stock_items(
    current_user: dict = Depends(get_current_user)
):
    """Get items that are out of stock"""
    try:
        items = db.get_low_stock_items('out_of_stock')
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/expiring")
async def get_expiring_items(
    days_ahead: int = Query(30, ge=1, le=365),
    current_user: dict = Depends(get_current_user)
):
    """Get items expiring within specified days"""
    try:
        items = db.get_expiring_items(days_ahead)
        return {"items": items, "days_ahead": days_ahead}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-adjustment")
async def bulk_stock_adjustment(
    adjustments: List[dict],
    reason: str,
    notes: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Perform bulk stock adjustments"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions for bulk adjustments")
        
        results = []
        
        for adjustment in adjustments:
            item_id = adjustment.get('item_id')
            new_quantity = adjustment.get('new_quantity')
            
            if not item_id or new_quantity is None:
                results.append({"item_id": item_id, "error": "Missing item_id or new_quantity"})
                continue
            
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
                movement_id = db.create_stock_movement(
                    item_id=item_id,
                    movement_type='ADJUSTMENT',
                    quantity=quantity_diff,
                    user_id=current_user['id'],
                    reference_type='bulk_adjustment',
                    reason=reason,
                    notes=notes
                )
                
                results.append({
                    "item_id": item_id, 
                    "old_quantity": current['quantity'],
                    "new_quantity": new_quantity,
                    "adjustment": quantity_diff,
                    "movement_id": movement_id,
                    "success": True
                })
            else:
                results.append({
                    "item_id": item_id,
                    "message": "No change required",
                    "success": True
                })
        
        return {"results": results, "total_processed": len(adjustments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/enhanced")
async def get_inventory_summary_enhanced_route(
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive inventory summary"""
    try:
        summary = get_inventory_summary_enhanced()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/valuation")
async def get_inventory_valuation(
    method: str = Query("AVERAGE", regex="^(FIFO|LIFO|AVERAGE|SPECIFIC)$"),
    as_of_date: Optional[date] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get inventory valuation using specified method"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions for valuation reports")
        
        if not as_of_date:
            as_of_date = date.today()
        
        # Calculate total valuation
        total_valuation = 0
        items_processed = 0
        
        # Get all active inventory items
        items = db.execute_query("""
            SELECT id, name_en, quantity, purchase_cost
            FROM inventory_items 
            WHERE is_active = 1 AND quantity > 0
        """, fetch_all=True)
        
        detailed_items = []
        
        for item in items:
            # Get stock movements with costs
            movements = db.execute_query("""
                SELECT quantity, unit_cost, created_at
                FROM stock_movements
                WHERE item_id = ? AND unit_cost IS NOT NULL 
                AND movement_type = 'IN' AND date(created_at) <= ?
                ORDER BY created_at
            """, (item['id'], as_of_date), fetch_all=True)
            
            if not movements:
                continue
            
            current_qty = item['quantity']
            
            if method == 'FIFO':
                # First In, First Out
                remaining_qty = current_qty
                total_cost = 0
                
                for movement in movements:
                    if remaining_qty <= 0:
                        break
                    
                    qty_to_use = min(remaining_qty, movement['quantity'])
                    total_cost += qty_to_use * movement['unit_cost']
                    remaining_qty -= qty_to_use
                
                cost_per_unit = total_cost / current_qty if current_qty > 0 else 0
            
            elif method == 'LIFO':
                # Last In, First Out
                remaining_qty = current_qty
                total_cost = 0
                
                for movement in reversed(movements):
                    if remaining_qty <= 0:
                        break
                    
                    qty_to_use = min(remaining_qty, movement['quantity'])
                    total_cost += qty_to_use * movement['unit_cost']
                    remaining_qty -= qty_to_use
                
                cost_per_unit = total_cost / current_qty if current_qty > 0 else 0
            
            else:  # AVERAGE
                total_cost = sum(m['quantity'] * m['unit_cost'] for m in movements)
                total_qty = sum(m['quantity'] for m in movements)
                cost_per_unit = total_cost / total_qty if total_qty > 0 else 0
            
            item_total_value = cost_per_unit * current_qty
            total_valuation += item_total_value
            items_processed += 1
            
            detailed_items.append({
                "item_id": item['id'],
                "item_name": item['name_en'],
                "quantity": current_qty,
                "cost_per_unit": round(cost_per_unit, 2),
                "total_value": round(item_total_value, 2)
            })
        
        return {
            "method": method,
            "as_of_date": as_of_date,
            "total_valuation": round(total_valuation, 2),
            "items_processed": items_processed,
            "currency": "NZD",
            "detailed_items": sorted(detailed_items, key=lambda x: x['total_value'], reverse=True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/barcode/{barcode}")
async def get_item_by_barcode(
    barcode: str,
    current_user: dict = Depends(get_current_user)
):
    """Get inventory item by barcode or SKU"""
    try:
        item = db.execute_query("""
            SELECT i.*, c.name_en as category_name_en, c.name_mi as category_name_mi,
                   l.name_en as location_name_en, l.name_mi as location_name_mi,
                   s.name as supplier_name
            FROM inventory_items i
            LEFT JOIN categories c ON i.category_id = c.id
            LEFT JOIN locations l ON i.location_id = l.id
            LEFT JOIN suppliers s ON i.supplier_id = s.id
            WHERE (i.barcode = ? OR i.sku = ?) AND i.is_active = 1
        """, (barcode, barcode), fetch_one=True)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/items/{item_id}/stock-in")
async def stock_in(
    item_id: int,
    stock_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Add stock to an inventory item"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get current item
            cursor.execute("SELECT * FROM inventory_items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            
            # Update quantity
            new_quantity = item[9] + stock_data.get('quantity', 0)  # quantity is at index 9
            cursor.execute(
                "UPDATE inventory_items SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_quantity, item_id)
            )
            
            # Record stock movement
            cursor.execute("""
                INSERT INTO stock_movements (
                    item_id, movement_type, quantity, to_location_id,
                    unit_cost, total_cost, user_id, reason, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id, 'IN', stock_data.get('quantity', 0), item[14],  # location_id at index 14
                stock_data.get('unit_cost', 0), 
                stock_data.get('unit_cost', 0) * stock_data.get('quantity', 0),
                current_user['id'], stock_data.get('reason', 'Stock In'), 
                stock_data.get('notes', '')
            ))
            
            conn.commit()
            
            return {
                "success": True,
                "message": "Stock added successfully",
                "new_quantity": new_quantity
            }
            
    except Exception as e:
        logger.error(f"Error in stock in: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/items/{item_id}/stock-out")
async def stock_out(
    item_id: int,
    stock_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Remove stock from an inventory item"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get current item
            cursor.execute("SELECT * FROM inventory_items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            
            # Check if enough stock available
            current_quantity = item[9]  # quantity is at index 9
            quantity_to_remove = stock_data.get('quantity', 0)
            
            if quantity_to_remove > current_quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient stock. Available: {current_quantity}, Requested: {quantity_to_remove}"
                )
            
            # Update quantity
            new_quantity = current_quantity - quantity_to_remove
            cursor.execute(
                "UPDATE inventory_items SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_quantity, item_id)
            )
            
            # Record stock movement
            cursor.execute("""
                INSERT INTO stock_movements (
                    item_id, movement_type, quantity, from_location_id,
                    user_id, reason, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id, 'OUT', quantity_to_remove, item[14],  # location_id at index 14
                current_user['id'], stock_data.get('reason', 'Stock Out'), 
                stock_data.get('notes', '')
            ))
            
            conn.commit()
            
            return {
                "success": True,
                "message": "Stock removed successfully",
                "new_quantity": new_quantity
            }
            
    except Exception as e:
        logger.error(f"Error in stock out: {e}")
        raise HTTPException(status_code=500, detail=str(e))