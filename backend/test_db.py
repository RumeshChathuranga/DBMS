print("Starting database test...")

import pymysql
from app.config import settings

print(f"Using DB settings: host={settings.DB_HOST}, user={settings.DB_USER}, db={settings.DB_NAME}")

try:
    conn = pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )
    print("✅ Database connected successfully")
    conn.close()
except Exception as e:
    print("❌ Database connection failed:", e)
