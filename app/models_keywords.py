from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Keyword(Base):
    __tablename__ = "keywords"

    __table_args__ = (
        UniqueConstraint("org_id", "keyword", name="uq_keywords_org_keyword"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="custom", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    store_keywords: Mapped[list["StoreKeyword"]] = relationship(
        back_populates="keyword_rel",
        cascade="all, delete-orphan",
    )


class StoreKeyword(Base):
    __tablename__ = "store_keywords"

    __table_args__ = (
        UniqueConstraint("store_id", "keyword_id", name="uq_store_keywords_store_keyword"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False, index=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keywords.id"), nullable=False, index=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    keyword_rel: Mapped["Keyword"] = relationship(back_populates="store_keywords")