"""
Main FastAPI Application
Entry point for the Hotel Reservation and Guest Services Management System
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.database.connection import Database

# Import all route modules
from app.api.routes import (
    auth,
    guests,
    rooms,
    reservations,
    services,
    billing,
    reports
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting HRGSMS API...")
    try:
        Database.initialize_pool()
        logger.info("✅ Database connection pool initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down HRGSMS API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Hotel Reservation and Guest Services Management System API",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,  # Use literal instead of status constant
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.DEBUG else "Internal server error"
        }
    )


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(guests.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")
app.include_router(reservations.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(billing.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "disabled",
        "message": "Welcome to HRGSMS API"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with Database.get_db_cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.APP_VERSION
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


# API information endpoint
@app.get("/api")
async def api_info():
    """API endpoints information"""
    return {
        "message": "HRGSMS API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "auth": "/api/auth",
            "guests": "/api/guests",
            "rooms": "/api/rooms",
            "reservations": "/api/reservations",
            "services": "/api/services",
            "billing": "/api/billing",
            "reports": "/api/reports"
        },
        "documentation": "/docs" if settings.DEBUG else "Contact administrator"
    }


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )