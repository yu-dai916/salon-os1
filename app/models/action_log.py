from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db import Base


class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)

    store_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)

    action_type = Column(String)  # review_reply / post_create など

    created_at = Column(DateTime, default=datetime.utcnow)