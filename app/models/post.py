from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    store_id = Column(Integer, nullable=False)

    status = Column(String(50), nullable=False)

    title = Column(String(255))

    content = Column(Text, nullable=False)

    source_title = Column(String(300))

    source_url = Column(String(600), nullable=False)

    google_post_id = Column(String(200))

    posted_at = Column(DateTime)

    last_error = Column(Text)

    created_at = Column(DateTime, server_default=func.now())

    org_id = Column(Integer, nullable=False, default=1)