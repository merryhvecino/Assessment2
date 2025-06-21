"""
Routes module for Kaiwhakarite Rawa
Centralized router exports
"""

from .auth_routes import router as auth_router
from .dashboard_routes import router as dashboard_router
from .inventory_routes import router as inventory_router
from .booking_routes import router as booking_router
from .purchase_order_routes import router as purchase_order_router
from .enhanced_inventory_routes import router as enhanced_inventory_router

__all__ = [
    "auth_router",
    "dashboard_router", 
    "inventory_router",
    "booking_router",
    "purchase_order_router",
    "enhanced_inventory_router"
] 