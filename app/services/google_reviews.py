import requests
import os

from app.db.session import SessionLocal
from app.models.review import Review


API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("PLACE_ID")


def fetch_and_save_reviews():
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={API_KEY}"

    res = requests.get(url)
    data = res.json()

    print("🔥 APIレスポンス:", data)

    reviews = data.get("result", {}).get("reviews", [])
    print("🔥 reviews:", reviews)

    db = SessionLocal()

    try:
        for r in reviews:
            print("🔥 INSERTする:", r.get("author_name"))

            review = Review(
                store_id=1,
                reviewer_name=r.get("author_name"),
                comment=r.get("text"),
                rating=r.get("rating"),
            )

            db.add(review)

        db.commit()
        print("✅ DB保存完了")

    except Exception as e:
        print("❌ DBエラー:", e)
        db.rollback()

    finally:
        db.close()
