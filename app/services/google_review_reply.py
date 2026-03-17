import requests
import os

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def send_reply(place_id, review_id, text):

    url = f"https://mybusiness.googleapis.com/v4/{place_id}/reviews/{review_id}/reply"

    data = {
        "comment": text
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.put(url, json=data, headers=headers)

    return r.json()