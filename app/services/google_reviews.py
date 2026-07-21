import os
import uuid
import requests

from app.db.session import SessionLocal
from app.models.review import Review
from app.models.store import Store


API_KEY = os.getenv("GOOGLE_API_KEY")


def fetch_and_save_reviews():
    print("🔥🔥🔥 ALL STORES MODE 🔥🔥🔥")

    db = SessionLocal()
    results = []

    try:
        stores = db.query(Store).all()
        print("🔥 STORES:", stores)

        for store in stores:
            if not store.place_id:
                print(f"⏩ {store.name}: place_idなし")
                continue

            print(f"🏪 店舗: {store.name}")

            url = (
                "https://maps.googleapis.com/maps/api/place/details/json"
                f"?place_id={store.place_id}&fields=reviews&key={API_KEY}"
            )

            res = requests.get(url)
            data = res.json()

            print("🔥 API:", data.get("status"))

            reviews = data.get("result", {}).get("reviews", [])
            print(f"🔥 reviews数: {len(reviews)}")

            new_count = 0

            for r in reviews:
                reviewer = r.get("author_name")
                comment = r.get("text")
                review_time = r.get("time")

                google_review_id = f"{reviewer}_{review_time}"

                exists = (
                    db.query(Review)
                    .filter(Review.google_review_id == google_review_id)
                    .first()
                )

                if exists:
                    continue

                review = Review(
                    id=uuid.uuid4().int % (2**63 - 1),
                    store_id=store.id,
                    reviewer_name=reviewer,
                    comment=comment,
                    rating=r.get("rating"),
                    google_review_id=google_review_id,
                )

                db.add(review)
                new_count += 1

            results.append(
                {
                    "store": store.name,
                    "new_count": new_count,
                }
            )

        db.commit()

    except Exception as e:
        print("❌ DBエラー:", e)
        db.rollback()

    finally:
        db.close()

    print("🔥 results:", results)
    return results

    print("🔥 results:", results)

    return results
