#!/usr/bin/env python3
"""
Dashboard routes for Kaiwhakarite Rawa
"""

from fastapi import APIRouter, Depends
from ..models import UserResponse
from ..auth import get_current_active_user
from ..services.dashboard_service import get_dashboard_statistics

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get dashboard statistics"""
    return get_dashboard_statistics() 