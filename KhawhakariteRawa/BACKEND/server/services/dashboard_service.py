#!/usr/bin/env python3
"""
Dashboard service for Kaiwhakarite Rawa
"""

from ..database import db


def get_dashboard_statistics():
    """Get dashboard statistics"""
    # Get basic statistics
    total_items_result = db.execute_query(
        "SELECT COUNT(*) as count FROM inventory_items",
        fetch_one=True
    )
    total_items = total_items_result['count'] if total_items_result else 0
    
    active_bookings_result = db.execute_query(
        "SELECT COUNT(*) as count FROM bookings WHERE status = 'Active'",
        fetch_one=True
    )
    active_bookings = (
        active_bookings_result['count'] if active_bookings_result else 0
    )
    
    pending_bookings_result = db.execute_query(
        "SELECT COUNT(*) as count FROM bookings WHERE status = 'Pending'",
        fetch_one=True
    )
    pending_bookings = (
        pending_bookings_result['count'] if pending_bookings_result else 0
    )
    
    maintenance_issues_result = db.execute_query(
        "SELECT COUNT(*) as count FROM maintenance_records " +
        "WHERE status = 'Pending'",
        fetch_one=True
    )
    maintenance_issues = (
        maintenance_issues_result['count'] if maintenance_issues_result else 0
    )
    
    # Get low stock items (quantity <= 5)
    low_stock_items_result = db.execute_query(
        "SELECT COUNT(*) as count FROM inventory_items WHERE quantity <= 5",
        fetch_one=True
    )
    low_stock_items = low_stock_items_result['count'] if low_stock_items_result else 0
    
    # Get total suppliers
    total_suppliers_result = db.execute_query(
        "SELECT COUNT(*) as count FROM suppliers",
        fetch_one=True
    )
    total_suppliers = total_suppliers_result['count'] if total_suppliers_result else 0
    
    # Get recent activities (last 10 bookings)
    recent_bookings = db.execute_query(
        """SELECT b.*, i.name_en as item_name, u.first_name, u.last_name
        FROM bookings b
        JOIN inventory_items i ON b.item_id = i.id
        JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
        LIMIT 10""",
        fetch_all=True
    ) or []
    
    # Get items by category for chart
    items_by_category = db.execute_query(
        """SELECT c.name_en as category, COUNT(i.id) as count
        FROM categories c
        LEFT JOIN inventory_items i ON c.id = i.category_id
        GROUP BY c.id, c.name_en
        ORDER BY count DESC""",
        fetch_all=True
    ) or []
    
    # Get booking status distribution
    booking_status_distribution = db.execute_query(
        """SELECT status, COUNT(*) as count
        FROM bookings
        GROUP BY status
        ORDER BY count DESC""",
        fetch_all=True
    ) or []
    
    # Get items by condition
    items_by_condition = db.execute_query(
        """SELECT condition_status, COUNT(*) as count
        FROM inventory_items
        GROUP BY condition_status
        ORDER BY count DESC""",
        fetch_all=True
    ) or []
    
    return {
        "total_items": total_items,
        "active_bookings": active_bookings,
        "pending_bookings": pending_bookings,
        "maintenance_issues": maintenance_issues,
        "low_stock_items": low_stock_items,
        "total_suppliers": total_suppliers,
        "recent_bookings": recent_bookings,
        "items_by_category": items_by_category,
        "booking_status_distribution": booking_status_distribution,
        "items_by_condition": items_by_condition
    } 