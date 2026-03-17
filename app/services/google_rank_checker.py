from app.services.google_serp import get_serp


def get_google_rank(keyword, place_id):

    results = get_serp(keyword)

    for r in results:

        if r["place_id"] == place_id:
            return r["position"]

    return None