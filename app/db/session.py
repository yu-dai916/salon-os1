import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_url():
    url = os.getenv("DATABASE_URL")
    print("🔥 DATABASE_URL (inside) =", url)
    if not url:
        raise Exception("❌ DATABASE_URLが空")
    return url

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
