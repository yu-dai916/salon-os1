import requests
from bs4 import BeautifulSoup


def get_google_rank(keyword):

    url = f"https://www.google.com/search?q={keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.select("div.g")

    rank = 1

    for result in results:

        link = result.find("a")

        if not link:
            continue

        href = link.get("href")

        if "hotpepper.jp" in href:
            return rank

        rank += 1

    return 100