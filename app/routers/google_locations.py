from fastapi import APIRouter
import requests
import os

router = APIRouter()

GOOGLE_API = "https://mybusinessbusinessinformation.googleapis.com/v1"


@router.get("/google/locations")
def get_locations(access_token: str):

    url = f"{GOOGLE_API}/accounts"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    res = requests.get(url, headers=headers)

    accounts = res.json()

    result = []

    for acc in accounts.get("accounts", []):

        acc_id = acc["name"]

        loc_url = f"{GOOGLE_API}/{acc_id}/locations"

        loc_res = requests.get(loc_url, headers=headers)

        locations = loc_res.json()

        for l in locations.get("locations", []):

            result.append({
                "name": l.get("title"),
                "place_id": l.get("metadata", {}).get("placeId")
            })

    return result