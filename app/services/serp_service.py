import os
import requests


API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def search_serp(query):

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": query,
        "key": API_KEY,
        "language": "ja"
    }

    r = requests.get(url, params=params)

    data = r.json()

    return data.get("results", [])