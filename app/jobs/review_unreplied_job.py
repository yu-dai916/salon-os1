from app.db.session import SessionLocal
from app.models.review import Review


def run():

    db = SessionLocal()

    reviews = (
        db.query(Review)
        .filter(Review.owner_reply_text == None)
        .order_by(Review.reviewed_at.desc())
        .limit(20)
        .all()
    )

    for r in reviews:
        print(f"[todo] reply needed store={r.store_id} review={r.review_text}")

    db.close()