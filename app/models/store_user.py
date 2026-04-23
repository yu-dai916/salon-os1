from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base

class StoreUser(Base):
    __tablename__ = "store_users"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

