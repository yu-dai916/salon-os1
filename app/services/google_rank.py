import os
import requests


SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_google_rank(keyword, target_domain):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google",
        "q": keyword,
        "hl": "ja",
        "num": 20,
        "api_key": SERPAPI_KEY,
    }

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    results = data.get("organic_results", [])

    for i, row in enumerate(results, start=1):
        link = row.get("link", "")
        if target_domain.lower() in link.lower():
            return i

    return 100