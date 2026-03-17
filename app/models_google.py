from sqlalchemy import String, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class GoogleToken(Base):
    __tablename__ = "google_tokens"

    __table_args__ = (
        UniqueConstraint("org_id", name="uq_google_tokens_org_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    access_token: Mapped[str] = mapped_column(String(2048), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(2048), nullable=True)
    token_type: Mapped[str] = mapped_column(String(50), nullable=True)
    scope: Mapped[str] = mapped_column(String(2048), nullable=True)

    expires_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )