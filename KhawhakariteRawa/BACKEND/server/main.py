#!/usr/bin/env python3
"""
Kaiwhakarite Rawa - Main FastAPI Application
Clean and modular architecture with separated concerns.
"""

import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path for direct execution
if __name__ == "__main__":
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))

# Dynamic imports to handle both direct execution and module imports
try:
    # Try relative imports first (when run as module)
    from .config import settings
    from .routes import (
        auth_router, dashboard_router, inventory_router, 
        booking_router, purchase_order_router, enhanced_inventory_router
    )
except ImportError:
    # Fall back to absolute imports (when run directly)
    from server.config import settings
    from server.routes.auth_routes import router as auth_router
    from server.routes.dashboard_routes import router as dashboard_router
    from server.routes.inventory_routes import router as inventory_router
    from server.routes.booking_routes import router as booking_router
    from server.routes.purchase_order_routes import (
        router as purchase_order_router
    )
    from server.routes.enhanced_inventory_routes import (
        router as enhanced_inventory_router
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Startup
    try:
        # Initialize database
        logger.info("Initializing database...")
        
        # Create upload directory if it doesn't exist
        Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        
        logger.info("Application startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Application shutdown")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add security middleware
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.kaiwhakarite.co.nz"]
        )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Mount static files
    try:
        app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), 
                name="uploads")
    except RuntimeError as e:
        logger.warning(f"Could not mount uploads directory: {e}")
    
    # Error handlers
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "message": "The requested resource was not found",
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Exception):
        logger.error(f"Internal server error: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An internal server error occurred"
            }
        )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "OK",
            "message": f"{settings.APP_NAME} API is running",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.APP_VERSION,
            "debug": settings.DEBUG
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.APP_NAME} API",
            "version": settings.APP_VERSION,
            "docs": "/docs" if settings.DEBUG else "Documentation disabled",
            "health": "/health"
        }
    
    # Register routers
    routers = [
        (auth_router, "Authentication"),
        (dashboard_router, "Dashboard"),
        (inventory_router, "Inventory"),
        (booking_router, "Bookings"),
        (purchase_order_router, "Purchase Orders"),
        (enhanced_inventory_router, "Enhanced Inventory")
    ]
    
    for router, name in routers:
        try:
            app.include_router(router)
            logger.info(f"Registered {name} routes")
        except Exception as e:
            logger.error(f"Failed to register {name} routes: {e}")
    
    return app


# Create the application instance
app = create_app()

# ============================================================================
# APPLICATION STARTUP FOR DIRECT EXECUTION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {settings.APP_NAME} API Server...")
    logger.info("Server will be available at:")
    logger.info("  - Local: http://localhost:8000")
    logger.info("  - Network: http://0.0.0.0:8000")
    logger.info("  - API Docs: http://localhost:8000/docs")
    logger.info("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info" if not settings.DEBUG else "debug",
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1) 
            