from app.db import get_db
from app.models import Store, Post
from app.services.formatter import format_for_google_post

try:
    from app.services.ai_post import generate_google_post_from_blog
    AI_POST_AVAILABLE = True
except Exception:
    AI_POST_AVAILABLE = False


def run(store_id: int, blog: dict):
    db = next(get_db())

    try:
        store = db.query(Store).filter(Store.id == store_id).first()
        if not store:
            return

        title = (blog.get("title") or "").strip()
        excerpt = (blog.get("excerpt") or "").strip()
        source_url = (blog.get("url") or "").strip()

        if not source_url:
            return

        try:
            if AI_POST_AVAILABLE:
                content = generate_google_post_from_blog(
                    title=title,
                    excerpt=excerpt,
                    source_url=source_url,
                    strategy_key=store.strategy_key,
                    phone_number=store.phone_number,
                    cta_url=store.cta_url,
                    store_name=store.name,
                )
            else:
                content = format_for_google_post(title, excerpt, source_url=source_url)
        except Exception as e:
            p_fail = Post(
                org_id=store.org_id,
                store_id=store.id,
                status="failed",
                content="(生成失敗)",
                source_title=title or None,
                source_url=source_url,
                last_error=str(e),
            )
            db.add(p_fail)
            db.commit()
            return

        p = Post(
            org_id=store.org_id,
            store_id=store.id,
            status="draft",
            content=content,
            source_title=title or None,
            source_url=source_url,
        )
        db.add(p)
        db.commit()

    finally:
        db.close()