from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)

    # 所属組織
    org_id = Column(Integer, index=True, nullable=False, default=1)

    # 基本情報
    store_code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    station = Column(String)

    # Google
    place_id = Column(String)

    # HPB
    hpb_url = Column(String)

    # 投稿設定
    post_interval_days = Column(Integer, default=2)
    strategy_key = Column(String, default="reservation_push")

    # CTA
    phone_number = Column(String)
    cta_url = Column(String)

    created_at = Column(TIMESTAMP, server_default=text("now()"))
