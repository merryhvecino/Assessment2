#!/usr/bin/env python3
"""
Booking routes for Kaiwhakarite Rawa
"""

from fastapi import APIRouter, Depends
from ..models import UserResponse, BookingCreate
from ..auth import get_current_active_user
from ..services.booking_service import get_user_bookings, create_booking

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("")
async def get_bookings(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get bookings based on user role"""
    bookings = get_user_bookings(current_user)
    return {"bookings": bookings}


@router.post("")
async def create_new_booking(
    booking: BookingCreate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Create a new booking"""
    created_booking = create_booking(booking, current_user)
    
    return {
        "message": "Booking created successfully",
        "booking": created_booking
    } 