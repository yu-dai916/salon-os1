from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    store_id = Column(Integer)

    title = Column(String(255))

    content = Column(Text)

    created_at = Column(DateTime, server_default=func.now())