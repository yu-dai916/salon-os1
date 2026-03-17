from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class Competitor(Base):

    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True)

    org_id = Column(Integer) 

    keyword = Column(String)

    name = Column(String)

    place_id = Column(String)

    rating = Column(Float)

    review_count = Column(Integer)

    position = Column(Integer)