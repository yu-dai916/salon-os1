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

    reviews = data.get("result", {}).get("reviews", [])

    db = SessionLocal()

    for r in reviews:
        review = Review(
            reviewer_name=r.get("author_name"),
            comment=r.get("text"),
            rating=r.get("rating"),
        )
        db.add(review)

    db.commit()
    db.close()