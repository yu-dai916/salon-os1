import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

print("🔥 DATABASE_URL =", DATABASE_URL)  # ←追加

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URLが空")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
