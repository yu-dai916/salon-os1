from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.review import Review
from app.models.task import Task

router = APIRouter(prefix="/dashboard")


@router.get("/{store_id}")
def get_dashboard(store_id: int, db: Session = Depends(get_db)):

    low_reviews = (
        db.query(Review)
        .filter(Review.store_id == store_id)
        .filter(Review.rating <= 2)
        .all()
    )

    unreplied = (
        db.query(Review)
        .filter(Review.store_id == store_id)
        .filter(Review.owner_reply_text == None)
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(Task.store_id == store_id)
        .all()
    )

    return {
        "low_reviews": low_reviews,
        "unreplied_reviews": unreplied,
        "tasks": tasks
    }