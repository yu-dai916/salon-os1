from app.db.session import SessionLocal
from app.models_competitor import Competitor
from app.services.google_serp import get_serp


def run():

    db = SessionLocal()

    keyword = "泉大津 美容室"

    results = get_serp(keyword)

    for r in results:

        c = Competitor(
            org_id=1,
            keyword=keyword,
            name=r["name"],
            place_id=r["place_id"],
            rating=r["rating"],
            review_count=r["review_count"],
            position=r["position"]
        )

        db.add(c)

    db.commit()
    db.close()

    print("[SERP] saved")