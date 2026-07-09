import requests
import os
import uuid

from app.db.session import SessionLocal
from app.models.review import Review


API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("PLACE_ID")


def fetch_and_save_reviews():
    print("🔥🔥🔥 NEW GOOGLE REVIEWS CODE 🔥🔥🔥")

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={API_KEY}"

    res = requests.get(url)
    data = res.json()

    print("🔥 APIレスポンス:", data)

    reviews = data.get("result", {}).get("reviews", [])
    print("🔥 reviews:", reviews)

    db = SessionLocal()

    new_count = 0  # 新規カウント

    try:
        for r in reviews:
            comment = r.get("text")

            # 🔥 重複チェック
            exists = db.query(Review).filter(
                Review.comment == comment
            ).first()

            if exists:
                print("⏩ スキップ:", r.get("author_name"))
                continue

            print("🔥 INSERTする:", r.get("author_name"))

            review = Review(
                id=uuid.uuid4().int % (2**63 - 1),
                store_id=1,
                reviewer_name=r.get("author_name"),
                comment=comment,
                rating=r.get("rating"),
            )

            db.add(review)
            new_count += 1

        db.commit()

        print(f"✅ 新規レビュー: {new_count}件")

    except Exception as e:
        print("❌ DBエラー:", e)
        db.rollback()
        new_count = 0  # エラー時は0扱い

    finally:
        db.close()

    return new_count  # 🔥 これ追加（超重要）
