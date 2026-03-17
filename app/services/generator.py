from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from app.models import Store, Post
from app.services.hpb import fetch_latest_blog
from app.services.formatter import format_for_google_post


def generate_draft_for_store(db: Session, store: Store) -> tuple[bool, str]:
    """
    下書き生成（店舗ごとの戦略/間隔/重複制約/事故検知を含む）
    return: (ok, msg_key)
    """

    if not store.hpb_url:
        return False, "hpb_url_empty"

    # ✅ 投稿間隔制御：最終 “posted扱い” から interval 未満なら生成しない
    interval_days = int(store.post_interval_days or 2)
    last_pub = (
        db.query(Post)
        .filter(Post.store_id == store.id, Post.status.in_(["approved", "posted"]))
        .order_by(desc(Post.posted_at), desc(Post.created_at))
        .first()
    )
    if last_pub:
        base_dt = last_pub.posted_at or last_pub.created_at
        if base_dt:
            # tz-aware -> naive に寄せる（utcで比較）
            try:
                base_dt_naive = base_dt.replace(tzinfo=None)
            except Exception:
                base_dt_naive = base_dt
            if datetime.utcnow() - base_dt_naive < timedelta(days=interval_days):
                return False, "interval_block"

    data = fetch_latest_blog(store.hpb_url)
    if data.get("debug"):
        return False, "hpb_parse_failed"

    source_url = (data.get("url") or "").strip()
    if not source_url:
        return False, "no_source_url"

    # ✅ 一覧URL事故検知（保存しない）
    if source_url.endswith("/blog/") or source_url.endswith("/blog"):
        return False, "list_url"

    content = format_for_google_post(
        data.get("title") or "",
        data.get("excerpt") or "",
        source_url,
        strategy_key=(store.strategy_key or "reservation_push"),
        cta_url=store.cta_url,
        phone_number=store.phone_number,
        store_name=store.name,
        store_code=store.store_code,
    )

    p = Post(
        store_id=store.id,
        status="draft",
        content=content,
        source_title=(data.get("title") or "").strip() or None,
        source_url=source_url,
    )

    db.add(p)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return False, "duplicate"

    return True, "created"