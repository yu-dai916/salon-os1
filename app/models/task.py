from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    store_id = Column(Integer)

    type = Column(String(50))

    title = Column(String(255))

    description = Column(Text)

    status = Column(String(50), default="open")

    created_at = Column(DateTime, server_default=func.now())