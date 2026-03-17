from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base


class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    keyword_id = Column(Integer)

    rank = Column(Integer)

    checked_at = Column(DateTime, server_default=func.now())