import requests
from app.db.session import SessionLocal
from app.models import Store, Review
import os

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
                    Review.google_review_id == r["time"]
                ).first()

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
                saved += 1

        except Exception as e:

            print("[reviews] error", store.name, e)

    db.commit()

    db.close()

    print(f"[reviews] saved={saved}")