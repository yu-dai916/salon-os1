from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base

class Agency(Base):
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)