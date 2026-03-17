from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db import Base
from app.models import Store


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    keyword = Column(Text)
    metric_date = Column(Date)

    google_rank = Column(Integer)
    hpb_clicks = Column(Integer)
    phone_calls = Column(Integer)

    created_at = Column(DateTime, server_default=func.now())