"""
Configuration Management
Loads environment variables and provides configuration settings
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application Settings"""
    
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "hrgsms_db")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY", 
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
    
    # Server Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:5173,http://localhost:3000"
    ).split(",")
    
    # Application Info
    APP_NAME: str = "Hotel Reservation and Guest Services Management System"
    APP_VERSION: str = "1.0.0"
    
    @property
    def database_url(self) -> str:
        """Generate database connection URL"""
        return f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Create settings instance
settings = Settings()


# For debugging - remove in production
if __name__ == "__main__":
    print("=== Configuration Settings ===")
    print(f"Database Host: {settings.DB_HOST}")
    print(f"Database Name: {settings.DB_NAME}")
    print(f"JWT Algorithm: {settings.JWT_ALGORITHM}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")