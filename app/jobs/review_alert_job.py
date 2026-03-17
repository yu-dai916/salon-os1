from app.db.session import SessionLocal
from app.models.review import Review


def run():

    db = SessionLocal()

    reviews = (
        db.query(Review)
        .filter(Review.rating <= 2)
        .order_by(Review.reviewed_at.desc())
        .limit(20)
        .all()
    )

    for r in reviews:
        print(f"[alert] low rating {r.store_id} {r.rating} {r.review_text}")

    db.close()