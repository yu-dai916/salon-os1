from app.db.session import SessionLocal
from app.models.store import Store
from app.models.task import Task
from app.services.serp_service import search_serp


def run():

    db = SessionLocal()

    stores = db.query(Store).all()

    for store in stores:

        query = f"{store.station} 美容室"

        results = search_serp(query)

        if not results:
            continue

        top = results[0]

        rating = top.get("rating", 0)
        reviews = top.get("user_ratings_total", 0)

        if reviews > 100:

            task = Task(
                store_id=store.id,
                type="serp_competitor",
                title="競合が強い",
                description=f"競合口コミ数 {reviews} 件"
            )

            db.add(task)

    db.commit()

    db.close()