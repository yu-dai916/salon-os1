from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base


class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True)

    agency_id = Column(
        Integer,
        ForeignKey("agencies.id"),
        nullable=True,
    )

    name = Column(String(255))
