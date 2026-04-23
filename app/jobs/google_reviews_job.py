import requests
import os

from sqlalchemy import func

from app.db.session import SessionLocal
from app.models import Store, Review
from app.services.review_task_service import create_review_task
from app.services.line_notify_service import notify_store_users

API_KEY = os.getenv("GOOGLE_API_KEY")


def run():

    db = SessionLocal()

    stores = db.query(Store).filter(Store.place_id != None).all()

    saved = 0

    for store in stores:

        try:

            url = "https://maps.googleapis.com/maps/api/place/details/json"

            params = {
                "place_id": store.place_id,
                "fields": "reviews",
                "key": API_KEY
            }

            res = requests.get(url, params=params).json()

            reviews = res.get("result", {}).get("reviews", [])

            for r in reviews:

                exists = db.query(Review).filter(
                    Review.google_review_id == str(r["time"])
                ).first()

                # 重複防止（本番はON）
                if exists:
                    continue

                review = Review(
                    store_id=store.id,
                    rating=r["rating"],
                    comment=r["text"],
                    reviewer_name=r["author_name"],
                    google_review_id=str(r["time"])
                )

                db.add(review)
                db.commit()
                db.refresh(review)

                # タスク生成
                create_review_task(db, review)

                # 🔥 危険口コミ（★2以下）即通知
                if review.rating and review.rating <= 2:
                    notify_store_users(
                        db,
                        review.store_id,
                        f"""【危険口コミ】
★{review.rating}の低評価あり

{(review.comment or "")[:30]}

今すぐ対応👇
http://localhost:8000/store/{review.store_id}/reviews
"""
                    )

                saved += 1

        except Exception as e:
            print("[reviews] error", store.name, e)

    # 🔥 未返信まとめ通知（ここが今回の追加）
    for store in stores:

        unreplied_count = db.query(func.count(Review.id))\
            .filter(Review.store_id == store.id)\
            .filter(Review.reply_text.is_(None))\
            .scalar()

        if unreplied_count and unreplied_count >= 3:
            notify_store_users(
                db,
                store.id,
                f"""【未返信口コミあり】
未返信が{unreplied_count}件あります

今すぐ対応👇
http://localhost:8000/store/{store.id}/reviews
"""
            )

    db.close()

    print(f"[reviews] saved={saved}")