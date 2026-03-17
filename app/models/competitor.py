from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Competitor(Base):

    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True)

    store_id = Column(Integer)

    name = Column(String(255))

    google_place_id = Column(String(255))