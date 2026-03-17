import os
import requests

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


class GooglePlacesService:

    BASE_URL = "https://maps.googleapis.com/maps/api/place"

    def search(self, query: str):

        url = f"{self.BASE_URL}/textsearch/json"

        params = {
            "query": query,
            "key": GOOGLE_MAPS_API_KEY,
            "language": "ja"
        }

        r = requests.get(url, params=params, timeout=10)

        data = r.json()

        print("[google_places status]", data.get("status"))

        return data.get("results", [])