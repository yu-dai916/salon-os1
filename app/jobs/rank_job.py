from app.db.session import SessionLocal
from app.models.store import Store
from app.models_meo import KeywordRanking
from app.services.google_rank_checker import get_google_rank


def run():

    db = SessionLocal()

    stores = db.query(Store).all()

    for store in stores:

        if not store.station:
            continue

        keyword = f"{store.station.replace('駅','')} 美容室"

        rank = get_google_rank(keyword, store.google_place_id)

        if rank:

            row = KeywordRanking(
                store_id=store.id,
                keyword=keyword,
                rank=rank
            )

            db.add(row)

            print(store.name, keyword, rank)

    db.commit()
    db.close()

    print("[rank] saved")