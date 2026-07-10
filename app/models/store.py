from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    place_id = Column(String)
    created_at = Column(TIMESTAMP, server_default=text("now()"))
