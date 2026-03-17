from .base import Base
from .session import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()