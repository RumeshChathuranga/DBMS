"""
Configuration Management
Loads environment variables and provides configuration settings
"""
from __future__ import annotations

import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Prefer backend/.env; fallback to auto-discovery if missing
BACKEND_DIR = Path(__file__).resolve().parents[1]  # ...\backend
ENV_FILE = BACKEND_DIR / ".env"

if ENV_FILE.is_file():
    load_dotenv(dotenv_path=ENV_FILE, override=True)
else:
    found = find_dotenv(usecwd=True)
    if found:
        load_dotenv(found, override=True)


class Settings:
    """Application Settings"""
    APP_NAME: str = os.getenv("APP_NAME","Hotel Reservation and Guest Services Management System")   
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "hrgsms_db")

    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))

    # Server Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").strip().lower() in {"1", "true", "yes", "on"}

    # CORS Configuration
    _cors_raw = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    )
    CORS_ORIGINS: List[str] = [o.strip() for o in _cors_raw.split(",") if o.strip()]

    # Application Info
    APP_NAME: str = os.getenv("APP_NAME", "Hotel Reservation and Guest Services Management System")

# Singleton settings instance
settings = Settings()


# For debugging - remove in production
if __name__ == "__main__":
    print("=== Configuration Settings ===")
    print(f"Database Host: {settings.DB_HOST}")
    print(f"Database Name: {settings.DB_NAME}")
    print(f"JWT Algorithm: {settings.JWT_ALGORITHM}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")
    print(f"DB_USER={settings.DB_USER}")
    print(f"DB_PASSWORD={settings.DB_PASSWORD}")
    print(f"DB_HOST={settings.DB_HOST}")
    print(f"DB_NAME={settings.DB_NAME}")