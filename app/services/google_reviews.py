import requests
import os
import uuid

from app.db.session import SessionLocal
from app.models.review import Review
from app.models.store import Store  # ←追加


API_KEY = os.getenv("GOOGLE_API_KEY")


def fetch_and_save_reviews():
    print("🔥🔥🔥 ALL STORES MODE 🔥🔥🔥")

    db = SessionLocal()

    results = []

    try:
        stores = db.query(Store).all()

        for store in stores:
            print(f"🏪 店舗: {store.name}")

            url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={store.place_id}&fields=reviews&key={API_KEY}"

            res = requests.get(url)
            data = res.json()

            reviews = data.get("result", {}).get("reviews", [])

            new_count = 0

            for r in reviews:
                comment = r.get("text")

                exists = db.query(Review).filter(
                    Review.comment == comment
                ).first()

                if exists:
                    continue

                review = Review(
                    id=uuid.uuid4().int % (2**63 - 1),
                    store_id=store.id,  # ←ここが超重要
                    reviewer_name=r.get("author_name"),
                    comment=comment,
                    rating=r.get("rating"),
                )

                db.add(review)
                new_count += 1

            results.append({
                "store": store.name,
                "new_count": new_count
            })

        db.commit()

    except Exception as e:
        print("❌ DBエラー:", e)
        db.rollback()

    finally:
        db.close()

    return results
