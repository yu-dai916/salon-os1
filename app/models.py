from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey,
    Boolean,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    stores = relationship("Store", back_populates="org")
class Store(Base):
    __tablename__ = "stores"
    __table_args__ = (
        UniqueConstraint("org_id", "store_code", name="uq_store_org_storecode"),
    )

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"), nullable=False)
    store_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    station = Column(String, nullable=True)
    hpb_url = Column(Text, nullable=True)
    post_interval_days = Column(Integer, default=2)
    strategy_key = Column(String, default="reservation_push")
    phone_number = Column(String, nullable=True)
    cta_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    google_place_id = Column(String, nullable=True)

    org = relationship("Org", back_populates="stores")

    posts: Mapped[list["Post"]] = relationship(
        back_populates="store",
        cascade="all, delete-orphan",
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="store",
        cascade="all, delete-orphan",
    )

    coupons: Mapped[list["Coupon"]] = relationship(
        back_populates="store",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("org_id", "store_code", name="uq_store_org_storecode"),
    )


class Post(Base):
    __tablename__ = "posts"

    __table_args__ = (
        UniqueConstraint("store_id", "source_url", name="uq_posts_store_sourceurl"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # SaaS分離キー（直接持つ）
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False, index=True)

    # draft / posted / failed / rejected
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    source_title: Mapped[str] = mapped_column(String(300), nullable=True)
    source_url: Mapped[str] = mapped_column(String(600), nullable=False)

    google_post_id: Mapped[str] = mapped_column(String(200), nullable=True)

    posted_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    store: Mapped["Store"] = relationship(back_populates="posts")


class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        UniqueConstraint("store_id", "google_review_id", name="uq_reviews_store_google_review_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # SaaS分離キー
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False, index=True)

    # Google側ID（冪等同期の鍵）
    google_review_id: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    reviewer_name: Mapped[str] = mapped_column(String(200), nullable=True)
    review_time: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=True)

    # pending → drafted → approved → sent
    reply_status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    reply_draft: Mapped[str] = mapped_column(Text, nullable=True)
    reply_text: Mapped[str] = mapped_column(Text, nullable=True)
    replied_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    store: Mapped["Store"] = relationship(back_populates="reviews")


class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # SaaS分離キー
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False, index=True)

    # draft / approved
    status: Mapped[str] = mapped_column(String(30), default="draft", nullable=False)

    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    expires_on: Mapped[str] = mapped_column(Date, nullable=False)
    cta_url: Mapped[str] = mapped_column(String(600), nullable=True)

    ai_suggestion: Mapped[str] = mapped_column(Text, nullable=True)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    store: Mapped["Store"] = relationship(back_populates="coupons")


class MetricMonthly(Base):
    __tablename__ = "metrics_monthly"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)

    month: Mapped[str] = mapped_column(String(7), nullable=False)  # "2026-02"
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    calls: Mapped[int] = mapped_column(Integer, default=0)
    website_clicks: Mapped[int] = mapped_column(Integer, default=0)
