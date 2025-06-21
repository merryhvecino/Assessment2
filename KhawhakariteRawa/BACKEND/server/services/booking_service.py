#!/usr/bin/env python3
"""
Booking service for Kaiwhakarite Rawa
"""

from datetime import date
from fastapi import HTTPException
from ..database import db
from ..models import BookingCreate, UserResponse


def get_user_bookings(current_user: UserResponse):
    """Get bookings based on user role"""
    if current_user.role in ['Admin', 'Manager', 'Kaimahi']:
        # Staff can see all bookings
        bookings = db.execute_query(
            """SELECT b.*, i.name_en as item_name, u.first_name, u.last_name,
                    approver.first_name as approver_first_name,
                    approver.last_name as approver_last_name
            FROM bookings b
            JOIN inventory_items i ON b.item_id = i.id
            JOIN users u ON b.user_id = u.id
            LEFT JOIN users approver ON b.approved_by = approver.id
            ORDER BY b.created_at DESC""",
            fetch_all=True
        )
    else:
        # Regular users can only see their own bookings
        bookings = db.execute_query(
            """SELECT b.*, i.name_en as item_name, u.first_name, u.last_name,
                    approver.first_name as approver_first_name,
                    approver.last_name as approver_last_name
            FROM bookings b
            JOIN inventory_items i ON b.item_id = i.id
            JOIN users u ON b.user_id = u.id
            LEFT JOIN users approver ON b.approved_by = approver.id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC""",
            (current_user.id,),
            fetch_all=True
        )
    
    return bookings


def create_booking(booking: BookingCreate, current_user: UserResponse):
    """Create a new booking"""
    # Check if item exists and is loanable
    item = db.execute_query(
        "SELECT * FROM inventory_items WHERE id = ? AND is_loanable = 1",
        (booking.item_id,),
        fetch_one=True
    )
    
    if not item:
        raise HTTPException(
            status_code=404, 
            detail="Item not found or not available for booking"
        )
    
    # Check if sufficient quantity is available
    if item['quantity'] < booking.quantity_requested:
        raise HTTPException(
            status_code=400, 
            detail=f"Only {item['quantity']} items available"
        )
    
    # Create booking
    booking_id = db.execute_query(
        """INSERT INTO bookings 
           (item_id, user_id, kaupapa_name, kaupapa_description, whanau_group,
            quantity_requested, booking_date, start_date, end_date, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (booking.item_id, current_user.id, booking.kaupapa_name,
         booking.kaupapa_description, booking.whanau_group,
         booking.quantity_requested, date.today(), booking.start_date,
         booking.end_date, booking.notes)
    )
    
    # Log audit
    db.log_audit(current_user.id, "CREATE", "bookings", booking_id, {}, 
                booking.dict())
    
    # Get created booking
    created_booking = db.execute_query(
        """SELECT b.*, i.name_en as item_name, u.first_name, u.last_name
        FROM bookings b
        JOIN inventory_items i ON b.item_id = i.id
        JOIN users u ON b.user_id = u.id
        WHERE b.id = ?""",
        (booking_id,),
        fetch_one=True
    )
    
    return created_booking 