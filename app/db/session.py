import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 強制 fallback（最終手段）
if not DATABASE_URL:
    print("⚠️ env取れてないから直書き使う")
    DATABASE_URL = "postgresql://postgres:Yudaifuji916%21@db.dmjzoetznpfcicwvujbt.supabase.co:5432/postgres"

print("🔥 DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
