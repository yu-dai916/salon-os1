from app.db.session import SessionLocal
from app.models.store import Store
from app.services.google_places_service import GooglePlacesService


def run():

    db = SessionLocal()
    service = GooglePlacesService()

    stores = db.query(Store).all()

    for store in stores:

        query = store.name

        print(f"[place] search: {query}")

        try:

            results = service.search(query)

            if not results:
                print(f"[place] not found {store.name}")
                continue

            place_id = results[0]["place_id"]

            store.google_place_id = place_id
            db.commit()

            print(f"[place] saved {store.name} {place_id}")

        except Exception as e:
            print(f"[place] error {store.name} {e}")

    db.close()