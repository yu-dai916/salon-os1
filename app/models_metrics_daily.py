from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class MetricDaily(Base):

    __tablename__ = "metrics_daily"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)

    keyword: Mapped[str] = mapped_column(String(200), nullable=False)

    rank: Mapped[int] = mapped_column(Integer)

    metric_date: Mapped[str] = mapped_column(Date)