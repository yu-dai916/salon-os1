from app.db.session import SessionLocal
from app.models.review import Review
from app.models.task import Task


def run():

    db = SessionLocal()

    reviews = (
        db.query(Review)
        .filter(Review.rating <= 2)
        .all()
    )

    for r in reviews:

        task = Task(
            store_id=r.store_id,
            type="review_reply",
            title="低評価レビュー返信",
            description=r.comment
        )

        db.add(task)

    db.commit()

    db.close()