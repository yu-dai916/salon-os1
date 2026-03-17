from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    store_id = Column(Integer)

    rating = Column(Integer)

    comment = Column(Text)

    reviewer_name = Column(String(200))

    review_time = Column(DateTime)

    reply_text = Column(Text)

    replied_at = Column(DateTime)

    google_review_id = Column(String(200))

    created_at = Column(DateTime, server_default=func.now())

    staff_name = Column(String)

    menu_name = Column(String)