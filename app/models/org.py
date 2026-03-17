from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Org(Base):

    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True)

    name = Column(String(255))