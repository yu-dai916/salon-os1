from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db import Base


class KeywordRanking(Base):

    __tablename__ = "keyword_rankings"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    keyword = Column(String)
    rank = Column(Integer)
    checked_at = Column(DateTime, default=datetime.utcnow)


class CompetitorMetric(Base):

    __tablename__ = "competitor_metrics"

    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    name = Column(String)
    rating = Column(Float)
    review_count = Column(Integer)
    rank = Column(Integer)
    checked_at = Column(DateTime, default=datetime.utcnow)