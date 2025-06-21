#!/usr/bin/env python3
"""
Inventory routes for Kaiwhakarite Rawa
"""

from typing import Optional
from fastapi import APIRouter, Depends
from ..models import UserResponse, InventoryItemCreate
from ..auth import get_current_active_user, require_staff
from ..services.inventory_service import get_inventory_items, create_inventory_item

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("")
async def get_inventory(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    location_id: Optional[int] = None,
    condition: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get inventory items with filtering and pagination"""
    return get_inventory_items(skip, limit, search, category_id, location_id, condition)


@router.post("")
async def create_item(
    item: InventoryItemCreate,
    current_user: UserResponse = Depends(require_staff)
):
    """Create a new inventory item"""
    created_item = create_inventory_item(item, current_user.id)
    
    return {
        "message": "Inventory item created successfully",
        "item": created_item
    } 