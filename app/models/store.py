from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class Store(Base):

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)

    store_code = Column(String(50))

    name = Column(String(255))

    place_id = Column(String)

    station = Column(String(255))

    hpb_url = Column(String(500))

    location_id = Column(String(255))

    post_interval_days = Column(Integer)

    strategy_key = Column(String(100))

    phone_number = Column(String(50))

    cta_url = Column(String(500))

    org_id = Column(Integer)

    created_at = Column(DateTime)

    google_place_id = Column(String(255))