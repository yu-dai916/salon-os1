import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("🔥🔥🔥 session.py 読まれてる 🔥🔥🔥")

# 👇 ここ絶対に順番守る
DATABASE_URL = os.getenv("DATABASE_URL")

print("🔥 env DATABASE_URL =", DATABASE_URL)

# 🔥 ここで止めるな（重要）
if not DATABASE_URL:
    print("⚠️ env取れてないから直書き使う")
    DATABASE_URL = "postgresql://postgres:Yudaifuji916%21@db.dmjzoetznpfcicwvujbt.supabase.co:5432/postgres"

print("🔥 最終 DATABASE_URL =", DATABASE_URL)

# 👇 ここまで来てから接続
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
