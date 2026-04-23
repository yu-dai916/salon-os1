# app/models/task.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    store_id = Column(Integer, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), index=True)

    type = Column(String(50), default="review_reply")

    title = Column(String(255))
    description = Column(Text)

    status = Column(String(50), default="open")  # open / in_progress / done

    priority = Column(String(50), default="normal")  # normal / danger

    assigned_to = Column(String(50), nullable=True)  # store / hq

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())