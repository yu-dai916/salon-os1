import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_google_competitors(keyword):

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google",
        "q": keyword,
        "hl": "ja",
        "num": 10,
        "api_key": SERPAPI_KEY,
    }

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()

    data = r.json()

    results = data.get("organic_results", [])

    competitors = []

    for row in results:
        title = row.get("title")
        link = row.get("link")

        competitors.append({
            "title": title,
            "link": link
        })

    return competitors