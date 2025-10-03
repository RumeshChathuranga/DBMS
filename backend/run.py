"""
Run script for HRGSMS API
Usage: python run.py
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 60)
    print("🏨 HRGSMS API Server")
    print("=" * 60)
    print(f"Host: {settings.API_HOST}")
    print(f"Port: {settings.API_PORT}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Database: {settings.DB_NAME}")
    print("=" * 60)
    print("\n📝 API Documentation will be available at:")
    print(f"   http://localhost:{settings.API_PORT}/docs")
    print(f"   http://localhost:{settings.API_PORT}/redoc")
    print("\n🔗 API Base URL:")
    print(f"   http://localhost:{settings.API_PORT}/api")
    print("\n⏹️  Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )