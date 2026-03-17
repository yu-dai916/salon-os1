from sqlalchemy import Column, Integer, Text
from app.db import Base


class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    name = Column(Text)