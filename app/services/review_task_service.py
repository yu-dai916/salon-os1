# app/services/review_task_service.py

from app.models.task import Task
from app.models.review import Review


def create_review_task(db, review: Review):

    exists = db.query(Task).filter(Task.review_id == review.id).first()
    if exists:
        return

    danger_keywords = ["最悪", "二度と", "返金", "クレーム", "ひどい"]

    priority = "danger" if any(
        k in (review.comment or "") for k in danger_keywords
    ) or (review.rating and review.rating <= 2) else "normal"

    task = Task(
        store_id=review.store_id,
        review_id=review.id,
        type="review_reply",
        title="口コミ返信対応",
        description=review.comment,
        priority=priority,
        status="open",
        assigned_to="store"
    )

    db.add(task)
    # ❌ commit / refresh 削除

    return task