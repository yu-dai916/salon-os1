import requests
import os

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_serp(keyword):

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": keyword,
        "key": API_KEY,
        "language": "ja"
    }

    r = requests.get(url, params=params)

    data = r.json()

    results = []

    for i, place in enumerate(data.get("results", [])[:10]):

        results.append({
            "position": i + 1,
            "name": place["name"],
            "place_id": place["place_id"],
            "rating": place.get("rating"),
            "review_count": place.get("user_ratings_total")
        })

    return results