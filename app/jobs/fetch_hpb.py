from sqlalchemy import func

from app.db import get_db
from app.models import Store, Post
from app.services.hpb import fetch_latest_blog
from app.queue import queue

TEST_STORE_IDS = [1, 2]


def run():
    db = next(get_db())

    print("DB CHECK:", db.query(Post).count())

    try:
        stores = (
            db.query(Store)
            .filter(Store.id.in_(TEST_STORE_IDS))
            .all()
        )

        print("===== FETCH HPB START =====")
        print("対象店舗数:", len(stores))

        for store in stores:
            print("\n--- STORE ---")
            print("ID:", store.id)
            print("NAME:", store.name)
            print("HPB URL:", store.hpb_url)

            if not store.hpb_url:
                print("❌ HPB URLなし → SKIP")
                continue

            data = fetch_latest_blog(store.hpb_url)
            print("BLOG DATA:", data)

            if not data:
                print("❌ データ取得失敗 → SKIP")
                continue

            source_url = (data.get("url") or "").strip()
            print("SOURCE URL:", source_url)

            if not source_url:
                print("❌ URLなし → SKIP")
                continue

            # 一覧URLチェック
            if source_url.endswith("/blog/") or source_url.endswith("/blog"):
                print("❌ 一覧URL → SKIP")
                continue

            # 重複チェック
            exists = (
                db.query(func.count(Post.id))
                .filter(Post.store_id == store.id, Post.source_url == source_url)
                .scalar()
            ) or 0

            print("EXISTS:", exists)

            if exists:
                print("❌ 既存データあり → SKIP")
                continue

            print("🔥 ENQUEUE 実行")

            queue.enqueue(
                "app.jobs.auto_post.run",
                store.id,
                {
                    "title": data.get("title"),
                    "excerpt": data.get("excerpt"),
                    "url": data.get("url"),

                    # AI用
                    "area": store.area,
                    "main_menu": store.main_menu,
                    "strategy_key": store.strategy_key,
                    "phone_number": store.phone_number,
                    "cta_url": store.cta_url,
                    "store_name": store.name,
                }
            )

        print("===== FETCH HPB END =====")

    finally:
        db.close()