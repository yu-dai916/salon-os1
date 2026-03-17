from sqlalchemy import func

from app.db import get_db
from app.models import Store, Post
from app.services.hpb import fetch_latest_blog
from app.queue import queue

TEST_STORE_IDS = [1, 2]


def run():
    db = next(get_db())

    try:
        stores = (
            db.query(Store)
            .filter(Store.id.in_(TEST_STORE_IDS))
            .all()
        )

        for store in stores:
            if not store.hpb_url:
                continue

            data = fetch_latest_blog(store.hpb_url)
            if not data:
                continue

            source_url = (data.get("url") or "").strip()
            if not source_url:
                continue

            # 一覧URLっぽいのは捨てる
            if source_url.endswith("/blog/") or source_url.endswith("/blog"):
                continue

            # 同じ元記事URLなら重複投入しない
            exists = (
                db.query(func.count(Post.id))
                .filter(Post.store_id == store.id, Post.source_url == source_url)
                .scalar()
            ) or 0

            if exists:
                continue

            queue.enqueue("app.jobs.auto_post.run", store.id, data)

    finally:
        db.close()