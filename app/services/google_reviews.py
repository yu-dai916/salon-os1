import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_google_reviews(place_id):

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_maps_reviews",
        "place_id": place_id,
        "api_key": SERPAPI_KEY,
        "hl": "ja"
    }

    r = requests.get(url, params=params)
    data = r.json()

    reviews = []

    for r in data.get("reviews", []):
        reviews.append({
            "review_id": r.get("review_id"),
            "rating": r.get("rating"),
            "comment": r.get("snippet"),
            "reviewer_name": r.get("user", {}).get("name"),
            "time": r.get("date")
        })

    return reviews