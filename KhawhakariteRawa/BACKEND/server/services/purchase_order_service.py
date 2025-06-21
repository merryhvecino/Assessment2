#!/usr/bin/env python3
"""
Purchase Order service for Kaiwhakarite Rawa
Handles purchase orders, goods receiving, and supplier management
"""

from typing import Optional, List
from datetime import date, datetime
from ..database import db
from ..models import (
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderStatus,
    MovementType
)


def generate_po_number():
    """Generate a unique purchase order number"""
    # Get the latest PO number
    latest_po = db.execute_query(
        "SELECT po_number FROM purchase_orders ORDER BY id DESC LIMIT 1",
        fetch_one=True
    )
    
    if latest_po and latest_po['po_number']:
        # Extract number from format PO-YYYY-NNNN
        try:
            last_number = int(latest_po['po_number'].split('-')[-1])
            next_number = last_number + 1
        except:
            next_number = 1
    else:
        next_number = 1
    
    # Format: PO-YYYY-NNNN
    current_year = datetime.now().year
    return f"PO-{current_year}-{next_number:04d}"


def create_purchase_order(po_data: PurchaseOrderCreate, user_id: int):
    """Create a new purchase order"""
    # Validate supplier exists
    supplier = db.execute_query(
        "SELECT * FROM suppliers WHERE id = ? AND is_active = 1",
        (po_data.supplier_id,), fetch_one=True
    )
    
    if not supplier:
        return {"error": "Supplier not found or inactive"}
    
    # Generate PO number
    po_number = generate_po_number()
    
    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in po_data.items)
    tax_amount = sum(item.quantity * item.unit_price * item.tax_rate for item in po_data.items)
    total_amount = subtotal + tax_amount
    
    # Create purchase order
    po_id = db.execute_query(
        """INSERT INTO purchase_orders 
           (po_number, supplier_id, status, order_date, expected_delivery_date,
            subtotal, tax_amount, total_amount, currency, payment_terms,
            shipping_address, billing_address, notes, created_by)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (po_number, po_data.supplier_id, PurchaseOrderStatus.DRAFT, 
         po_data.order_date, po_data.expected_delivery_date,
         subtotal, tax_amount, total_amount, supplier['currency'],
         po_data.payment_terms or supplier['payment_terms'],
         po_data.shipping_address, po_data.billing_address,
         po_data.notes, user_id)
    )
    
    # Create purchase order items
    for item in po_data.items:
        total_price = item.quantity * item.unit_price
        db.execute_query(
            """INSERT INTO purchase_order_items 
               (po_id, item_id, description, quantity, unit_price, total_price, tax_rate, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (po_id, item.item_id, item.description, item.quantity, 
             item.unit_price, total_price, item.tax_rate, item.notes)
        )
    
    # Log audit
    db.log_audit(user_id, "CREATE", "purchase_orders", po_id, {}, po_data.dict())
    
    # Create financial transaction record
    db.execute_query(
        """INSERT INTO financial_transactions 
           (transaction_type, reference_id, reference_type, amount, currency,
            tax_amount, tax_rate, description, transaction_date, status, created_by)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ('PURCHASE', po_id, 'purchase_order', total_amount, supplier['currency'],
         tax_amount, 0.15, f'Purchase Order {po_number}', po_data.order_date,
         'PENDING', user_id)
    )
    
    return get_purchase_order_by_id(po_id)


def get_purchase_orders(skip: int = 0, limit: int = 100, supplier_id: Optional[int] = None,
                       status: Optional[str] = None, date_from: Optional[date] = None,
                       date_to: Optional[date] = None):
    """Get purchase orders with filtering"""
    query = """
        SELECT po.*, s.name as supplier_name, s.contact_person, s.email as supplier_email,
               u.first_name || ' ' || u.last_name as created_by_name,
               a.first_name || ' ' || a.last_name as approved_by_name
        FROM purchase_orders po
        JOIN suppliers s ON po.supplier_id = s.id
        JOIN users u ON po.created_by = u.id
        LEFT JOIN users a ON po.approved_by = a.id
        WHERE 1=1
    """
    
    params = []
    
    if supplier_id:
        query += " AND po.supplier_id = ?"
        params.append(supplier_id)
    
    if status:
        query += " AND po.status = ?"
        params.append(status)
    
    if date_from:
        query += " AND po.order_date >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND po.order_date <= ?"
        params.append(date_to)
    
    query += " ORDER BY po.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, skip])
    
    orders = db.execute_query(query, tuple(params), fetch_all=True)
    
    # Get total count
    count_query = "SELECT COUNT(*) FROM purchase_orders po WHERE 1=1"
    count_params = []
    
    if supplier_id:
        count_query += " AND po.supplier_id = ?"
        count_params.append(supplier_id)
    
    if status:
        count_query += " AND po.status = ?"
        count_params.append(status)
    
    if date_from:
        count_query += " AND po.order_date >= ?"
        count_params.append(date_from)
    
    if date_to:
        count_query += " AND po.order_date <= ?"
        count_params.append(date_to)
    
    total = db.execute_query(count_query, tuple(count_params), fetch_one=True)[0]
    
    return {
        "orders": orders,
        "total": total,
        "skip": skip,
        "limit": limit
    }


def get_purchase_order_by_id(po_id: int):
    """Get purchase order with items"""
    po = db.execute_query("""
        SELECT po.*, s.name as supplier_name, s.contact_person, s.email as supplier_email,
               s.phone as supplier_phone, s.address as supplier_address,
               u.first_name || ' ' || u.last_name as created_by_name,
               a.first_name || ' ' || a.last_name as approved_by_name
        FROM purchase_orders po
        JOIN suppliers s ON po.supplier_id = s.id
        JOIN users u ON po.created_by = u.id
        LEFT JOIN users a ON po.approved_by = a.id
        WHERE po.id = ?
    """, (po_id,), fetch_one=True)
    
    if not po:
        return None
    
    # Get items
    items = db.execute_query("""
        SELECT poi.*, i.name_en as item_name, i.sku, i.barcode
        FROM purchase_order_items poi
        LEFT JOIN inventory_items i ON poi.item_id = i.id
        WHERE poi.po_id = ?
        ORDER BY poi.id
    """, (po_id,), fetch_all=True)
    
    # Get GRNs
    grns = db.execute_query("""
        SELECT grn.*, u.first_name || ' ' || u.last_name as received_by_name
        FROM goods_received_notes grn
        JOIN users u ON grn.received_by = u.id
        WHERE grn.po_id = ?
        ORDER BY grn.received_date DESC
    """, (po_id,), fetch_all=True)
    
    return {
        **po,
        "items": items,
        "grns": grns
    }


def update_purchase_order(po_id: int, po_update: PurchaseOrderUpdate, user_id: int):
    """Update purchase order"""
    # Get current PO
    current_po = db.execute_query(
        "SELECT * FROM purchase_orders WHERE id = ?",
        (po_id,), fetch_one=True
    )
    
    if not current_po:
        return {"error": "Purchase order not found"}
    
    # Check if PO can be updated
    if current_po['status'] in [PurchaseOrderStatus.RECEIVED, PurchaseOrderStatus.CANCELLED]:
        return {"error": "Cannot update completed or cancelled purchase order"}
    
    # Build update query
    update_fields = []
    params = []
    
    for field, value in po_update.dict(exclude_unset=True).items():
        if field == 'status' and value == PurchaseOrderStatus.CONFIRMED:
            update_fields.extend(['status = ?', 'approved_by = ?', 'approved_at = CURRENT_TIMESTAMP'])
            params.extend([value, user_id])
        else:
            update_fields.append(f"{field} = ?")
            params.append(value)
    
    if not update_fields:
        return get_purchase_order_by_id(po_id)
    
    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    params.append(po_id)
    
    # Execute update
    db.execute_query(
        f"UPDATE purchase_orders SET {', '.join(update_fields)} WHERE id = ?",
        tuple(params)
    )
    
    # Log audit
    db.log_audit(user_id, "UPDATE", "purchase_orders", po_id, 
                 current_po, po_update.dict(exclude_unset=True))
    
    return get_purchase_order_by_id(po_id)


def create_goods_received_note(po_id: int, received_items: List[dict], user_id: int):
    """Create goods received note and update inventory"""
    # Validate PO exists and is confirmed
    po = db.execute_query(
        "SELECT * FROM purchase_orders WHERE id = ? AND status = ?",
        (po_id, PurchaseOrderStatus.CONFIRMED), fetch_one=True
    )
    
    if not po:
        return {"error": "Purchase order not found or not confirmed"}
    
    # Generate GRN number
    grn_number = f"GRN-{datetime.now().strftime('%Y%m%d')}-{po_id:04d}"
    
    # Create GRN
    grn_id = db.execute_query(
        """INSERT INTO goods_received_notes 
           (grn_number, po_id, received_date, received_by, status)
           VALUES (?, ?, ?, ?, ?)""",
        (grn_number, po_id, date.today(), user_id, 'PENDING')
    )
    
    total_received = 0
    
    # Process received items
    for item_data in received_items:
        po_item_id = item_data['po_item_id']
        quantity_received = item_data['quantity_received']
        condition_status = item_data.get('condition_status', 'Good')
        expiry_date = item_data.get('expiry_date')
        batch_number = item_data.get('batch_number')
        notes = item_data.get('notes')
        
        # Get PO item details
        po_item = db.execute_query(
            "SELECT * FROM purchase_order_items WHERE id = ?",
            (po_item_id,), fetch_one=True
        )
        
        if not po_item:
            continue
        
        # Create GRN item
        db.execute_query(
            """INSERT INTO grn_items 
               (grn_id, po_item_id, quantity_received, condition_status, 
                expiry_date, batch_number, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (grn_id, po_item_id, quantity_received, condition_status,
             expiry_date, batch_number, notes)
        )
        
        # Update PO item received quantity
        db.execute_query(
            "UPDATE purchase_order_items SET received_quantity = received_quantity + ? WHERE id = ?",
            (quantity_received, po_item_id)
        )
        
        # Update inventory if item exists
        if po_item['item_id']:
            # Create stock movement
            db.create_stock_movement(
                item_id=po_item['item_id'],
                movement_type=MovementType.IN,
                quantity=quantity_received,
                user_id=user_id,
                reference_id=po_id,
                reference_type='purchase_order',
                unit_cost=po_item['unit_price'],
                total_cost=po_item['unit_price'] * quantity_received,
                reason=f'Goods received from PO {po["po_number"]}',
                notes=f'GRN: {grn_number}'
            )
            
            # Update item details if provided
            update_fields = []
            update_params = []
            
            if condition_status and condition_status != 'Good':
                update_fields.append('condition_status = ?')
                update_params.append(condition_status)
            
            if expiry_date:
                update_fields.append('expiry_date = ?')
                update_params.append(expiry_date)
            
            if update_fields:
                update_params.append(po_item['item_id'])
                db.execute_query(
                    f"UPDATE inventory_items SET {', '.join(update_fields)} WHERE id = ?",
                    tuple(update_params)
                )
            
            # Update inventory valuation
            db.update_inventory_valuation(po_item['item_id'], 'AVERAGE')
        
        total_received += quantity_received
    
    # Check if PO is fully received
    po_items_status = db.execute_query("""
        SELECT SUM(quantity) as total_ordered, SUM(received_quantity) as total_received
        FROM purchase_order_items WHERE po_id = ?
    """, (po_id,), fetch_one=True)
    
    if po_items_status['total_received'] >= po_items_status['total_ordered']:
        # Mark PO as received
        db.execute_query(
            "UPDATE purchase_orders SET status = ?, actual_delivery_date = ? WHERE id = ?",
            (PurchaseOrderStatus.RECEIVED, date.today(), po_id)
        )
    elif po_items_status['total_received'] > 0:
        # Mark as partially received
        db.execute_query(
            "UPDATE purchase_orders SET status = ? WHERE id = ?",
            (PurchaseOrderStatus.PARTIALLY_RECEIVED, po_id)
        )
    
    # Update financial transaction
    db.execute_query("""
        UPDATE financial_transactions 
        SET status = 'COMPLETED' 
        WHERE reference_id = ? AND reference_type = 'purchase_order'
    """, (po_id,))
    
    # Log audit
    db.log_audit(user_id, "CREATE", "goods_received_notes", grn_id, {}, {
        "grn_number": grn_number,
        "po_id": po_id,
        "items_received": len(received_items),
        "total_quantity": total_received
    })
    
    return {
        "grn_id": grn_id,
        "grn_number": grn_number,
        "message": f"Goods received note created successfully. {total_received} items received."
    }


def get_supplier_performance(supplier_id: Optional[int] = None, days_back: int = 365):
    """Get supplier performance metrics"""
    query = """
        SELECT s.id, s.name, s.rating,
               COUNT(po.id) as total_orders,
               SUM(po.total_amount) as total_value,
               AVG(julianday(po.actual_delivery_date) - julianday(po.expected_delivery_date)) as avg_delay_days,
               COUNT(CASE WHEN po.status = 'RECEIVED' THEN 1 END) as completed_orders,
               COUNT(CASE WHEN po.actual_delivery_date <= po.expected_delivery_date THEN 1 END) as on_time_deliveries
        FROM suppliers s
        LEFT JOIN purchase_orders po ON s.id = po.supplier_id 
            AND po.created_at >= date('now', '-' || ? || ' days')
        WHERE s.is_active = 1
    """
    
    params = [days_back]
    
    if supplier_id:
        query += " AND s.id = ?"
        params.append(supplier_id)
    
    query += " GROUP BY s.id, s.name, s.rating ORDER BY total_value DESC"
    
    return db.execute_query(query, tuple(params), fetch_all=True)


def get_purchase_order_summary():
    """Get purchase order summary statistics"""
    summary = {}
    
    # Basic counts
    summary['total_orders'] = db.execute_query(
        "SELECT COUNT(*) as count FROM purchase_orders",
        fetch_one=True
    )['count']
    
    summary['pending_orders'] = db.execute_query(
        "SELECT COUNT(*) as count FROM purchase_orders WHERE status IN ('DRAFT', 'SENT', 'CONFIRMED')",
        fetch_one=True
    )['count']
    
    summary['total_value'] = db.execute_query(
        "SELECT SUM(total_amount) as total FROM purchase_orders WHERE status != 'CANCELLED'",
        fetch_one=True
    )['total'] or 0
    
    # By status
    summary['by_status'] = db.execute_query("""
        SELECT status, COUNT(*) as count, SUM(total_amount) as total_value
        FROM purchase_orders
        GROUP BY status
        ORDER BY count DESC
    """, fetch_all=True)
    
    # By supplier
    summary['by_supplier'] = db.execute_query("""
        SELECT s.name as supplier, COUNT(po.id) as count, SUM(po.total_amount) as total_value
        FROM purchase_orders po
        JOIN suppliers s ON po.supplier_id = s.id
        GROUP BY s.id, s.name
        ORDER BY total_value DESC
        LIMIT 10
    """, fetch_all=True)
    
    return summary