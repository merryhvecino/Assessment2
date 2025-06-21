#!/usr/bin/env python3
"""
Purchase Order routes for Kaiwhakarite Rawa
Handles purchase orders, goods receiving, and supplier management
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from datetime import date
from ..auth import get_current_user
from ..models import (
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse,
    SupplierCreate, SupplierUpdate, SupplierResponse
)
from ..services.purchase_order_service import (
    create_purchase_order, get_purchase_orders, get_purchase_order_by_id,
    update_purchase_order, create_goods_received_note, get_supplier_performance,
    get_purchase_order_summary
)
from ..database import db

router = APIRouter(prefix="/api/purchase-orders", tags=["Purchase Orders"])


@router.post("/", response_model=dict)
async def create_purchase_order_route(
    po_data: PurchaseOrderCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new purchase order"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions to create purchase orders")
        
        result = create_purchase_order(po_data, current_user['id'])
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def get_purchase_orders_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supplier_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get purchase orders with filtering"""
    try:
        result = get_purchase_orders(
            skip=skip,
            limit=limit,
            supplier_id=supplier_id,
            status=status,
            date_from=date_from,
            date_to=date_to
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{po_id}", response_model=dict)
async def get_purchase_order_by_id_route(
    po_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get purchase order by ID with items and GRNs"""
    try:
        po = get_purchase_order_by_id(po_id)
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return po
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{po_id}", response_model=dict)
async def update_purchase_order_route(
    po_id: int,
    po_update: PurchaseOrderUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update purchase order"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions to update purchase orders")
        
        result = update_purchase_order(po_id, po_update, current_user['id'])
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{po_id}/receive", response_model=dict)
async def create_goods_received_note_route(
    po_id: int,
    received_items: List[dict],
    current_user: dict = Depends(get_current_user)
):
    """Create goods received note and update inventory"""
    try:
        if current_user['role'] not in ['Admin', 'Manager', 'Kaimahi']:
            raise HTTPException(status_code=403, detail="Insufficient permissions to receive goods")
        
        result = create_goods_received_note(po_id, received_items, current_user['id'])
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/statistics")
async def get_purchase_order_summary_route(
    current_user: dict = Depends(get_current_user)
):
    """Get purchase order summary statistics"""
    try:
        summary = get_purchase_order_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Supplier routes
@router.post("/suppliers/", response_model=dict)
async def create_supplier(
    supplier: SupplierCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new supplier"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions to create suppliers")
        
        # Create supplier
        supplier_id = db.execute_query(
            """INSERT INTO suppliers 
               (name, contact_person, email, phone, address, website, tax_number,
                payment_terms, currency, is_active, rating, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (supplier.name, supplier.contact_person, supplier.email, supplier.phone,
             supplier.address, supplier.website, supplier.tax_number, supplier.payment_terms,
             supplier.currency, supplier.is_active, supplier.rating, supplier.notes)
        )
        
        # Log audit
        db.log_audit(current_user['id'], "CREATE", "suppliers", supplier_id, {}, supplier.dict())
        
        # Get created supplier
        created_supplier = db.execute_query(
            "SELECT * FROM suppliers WHERE id = ?",
            (supplier_id,), fetch_one=True
        )
        
        return created_supplier
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suppliers/", response_model=dict)
async def get_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = Query(True),
    search: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get suppliers with filtering"""
    try:
        query = """
            SELECT s.*, 
                   COUNT(po.id) as total_orders,
                   SUM(po.total_amount) as total_value,
                   MAX(po.created_at) as last_order_date
            FROM suppliers s
            LEFT JOIN purchase_orders po ON s.id = po.supplier_id
            WHERE 1=1
        """
        
        params = []
        
        if is_active is not None:
            query += " AND s.is_active = ?"
            params.append(1 if is_active else 0)
        
        if search:
            search_param = f"%{search}%"
            query += " AND (s.name LIKE ? OR s.contact_person LIKE ? OR s.email LIKE ?)"
            params.extend([search_param, search_param, search_param])
        
        query += " GROUP BY s.id ORDER BY s.name LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        suppliers = db.execute_query(query, tuple(params), fetch_all=True)
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM suppliers s WHERE 1=1"
        count_params = []
        
        if is_active is not None:
            count_query += " AND s.is_active = ?"
            count_params.append(1 if is_active else 0)
        
        if search:
            count_query += " AND (s.name LIKE ? OR s.contact_person LIKE ? OR s.email LIKE ?)"
            count_params.extend([search_param, search_param, search_param])
        
        total = db.execute_query(count_query, tuple(count_params), fetch_one=True)[0]
        
        return {
            "suppliers": suppliers,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suppliers/{supplier_id}", response_model=dict)
async def get_supplier_by_id(
    supplier_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get supplier by ID with performance metrics"""
    try:
        supplier = db.execute_query(
            "SELECT * FROM suppliers WHERE id = ?",
            (supplier_id,), fetch_one=True
        )
        
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Get recent purchase orders
        recent_orders = db.execute_query("""
            SELECT po.*, u.first_name || ' ' || u.last_name as created_by_name
            FROM purchase_orders po
            JOIN users u ON po.created_by = u.id
            WHERE po.supplier_id = ?
            ORDER BY po.created_at DESC
            LIMIT 10
        """, (supplier_id,), fetch_all=True)
        
        # Get performance metrics
        performance = get_supplier_performance(supplier_id, 365)
        
        # Get price lists
        price_lists = db.execute_query("""
            SELECT spl.*, i.name_en as item_name
            FROM supplier_price_lists spl
            LEFT JOIN inventory_items i ON spl.item_id = i.id
            WHERE spl.supplier_id = ? AND spl.is_active = 1
            ORDER BY spl.item_description, spl.unit_price
        """, (supplier_id,), fetch_all=True)
        
        return {
            **supplier,
            "recent_orders": recent_orders,
            "performance": performance[0] if performance else None,
            "price_lists": price_lists
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/suppliers/{supplier_id}", response_model=dict)
async def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update supplier"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions to update suppliers")
        
        # Get current supplier
        current_supplier = db.execute_query(
            "SELECT * FROM suppliers WHERE id = ?",
            (supplier_id,), fetch_one=True
        )
        
        if not current_supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Build update query
        update_fields = []
        params = []
        
        for field, value in supplier_update.dict(exclude_unset=True).items():
            update_fields.append(f"{field} = ?")
            params.append(value)
        
        if not update_fields:
            return current_supplier
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(supplier_id)
        
        # Execute update
        db.execute_query(
            f"UPDATE suppliers SET {', '.join(update_fields)} WHERE id = ?",
            tuple(params)
        )
        
        # Log audit
        db.log_audit(current_user['id'], "UPDATE", "suppliers", supplier_id,
                     current_supplier, supplier_update.dict(exclude_unset=True))
        
        # Get updated supplier
        updated_supplier = db.execute_query(
            "SELECT * FROM suppliers WHERE id = ?",
            (supplier_id,), fetch_one=True
        )
        
        return updated_supplier
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suppliers/performance/report")
async def get_supplier_performance_report(
    supplier_id: Optional[int] = Query(None),
    days_back: int = Query(365, ge=30, le=1095),
    current_user: dict = Depends(get_current_user)
):
    """Get supplier performance report"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions for performance reports")
        
        performance = get_supplier_performance(supplier_id, days_back)
        return {
            "period_days": days_back,
            "suppliers": performance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suppliers/{supplier_id}/price-lists", response_model=dict)
async def create_supplier_price_list(
    supplier_id: int,
    price_list_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Create supplier price list entry"""
    try:
        if current_user['role'] not in ['Admin', 'Manager']:
            raise HTTPException(status_code=403, detail="Insufficient permissions to manage price lists")
        
        # Validate supplier exists
        supplier = db.execute_query(
            "SELECT id FROM suppliers WHERE id = ? AND is_active = 1",
            (supplier_id,), fetch_one=True
        )
        
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found or inactive")
        
        # Create price list entry
        price_list_id = db.execute_query(
            """INSERT INTO supplier_price_lists 
               (supplier_id, item_id, item_description, supplier_sku, unit_price,
                currency, minimum_order_quantity, lead_time_days, valid_from,
                valid_to, is_active, discount_percentage, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (supplier_id, price_list_data.get('item_id'), price_list_data.get('item_description'),
             price_list_data.get('supplier_sku'), price_list_data['unit_price'],
             price_list_data.get('currency', 'NZD'), price_list_data.get('minimum_order_quantity', 1),
             price_list_data.get('lead_time_days', 7), price_list_data.get('valid_from'),
             price_list_data.get('valid_to'), price_list_data.get('is_active', True),
             price_list_data.get('discount_percentage', 0), price_list_data.get('notes'))
        )
        
        # Log audit
        db.log_audit(current_user['id'], "CREATE", "supplier_price_lists", price_list_id, {}, price_list_data)
        
        # Get created price list entry
        created_entry = db.execute_query(
            "SELECT * FROM supplier_price_lists WHERE id = ?",
            (price_list_id,), fetch_one=True
        )
        
        return created_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/grn/", response_model=dict)
async def get_goods_received_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    po_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get goods received notes"""
    try:
        query = """
            SELECT grn.*, po.po_number, s.name as supplier_name,
                   u.first_name || ' ' || u.last_name as received_by_name
            FROM goods_received_notes grn
            JOIN purchase_orders po ON grn.po_id = po.id
            JOIN suppliers s ON po.supplier_id = s.id
            JOIN users u ON grn.received_by = u.id
            WHERE 1=1
        """
        
        params = []
        
        if po_id:
            query += " AND grn.po_id = ?"
            params.append(po_id)
        
        if date_from:
            query += " AND grn.received_date >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND grn.received_date <= ?"
            params.append(date_to)
        
        query += " ORDER BY grn.received_date DESC LIMIT ? OFFSET ?"
        params.extend([limit, skip])
        
        grns = db.execute_query(query, tuple(params), fetch_all=True)
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM goods_received_notes grn WHERE 1=1"
        count_params = []
        
        if po_id:
            count_query += " AND grn.po_id = ?"
            count_params.append(po_id)
        
        if date_from:
            count_query += " AND grn.received_date >= ?"
            count_params.append(date_from)
        
        if date_to:
            count_query += " AND grn.received_date <= ?"
            count_params.append(date_to)
        
        total = db.execute_query(count_query, tuple(count_params), fetch_one=True)[0]
        
        return {
            "grns": grns,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/grn/{grn_id}", response_model=dict)
async def get_goods_received_note_by_id(
    grn_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get goods received note by ID with items"""
    try:
        grn = db.execute_query("""
            SELECT grn.*, po.po_number, s.name as supplier_name,
                   u.first_name || ' ' || u.last_name as received_by_name
            FROM goods_received_notes grn
            JOIN purchase_orders po ON grn.po_id = po.id
            JOIN suppliers s ON po.supplier_id = s.id
            JOIN users u ON grn.received_by = u.id
            WHERE grn.id = ?
        """, (grn_id,), fetch_one=True)
        
        if not grn:
            raise HTTPException(status_code=404, detail="GRN not found")
        
        # Get GRN items
        items = db.execute_query("""
            SELECT gi.*, poi.description, poi.unit_price, i.name_en as item_name
            FROM grn_items gi
            JOIN purchase_order_items poi ON gi.po_item_id = poi.id
            LEFT JOIN inventory_items i ON poi.item_id = i.id
            WHERE gi.grn_id = ?
        """, (grn_id,), fetch_all=True)
        
        return {
            **grn,
            "items": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))