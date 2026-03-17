from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db import get_db
from app.models.store import Store
from app.models.post import Post
from app.models.review import Review
from app.models.task import Task

router = APIRouter(prefix="/hq")


@router.get("/overview")
def hq_overview(db: Session = Depends(get_db)):

    stores = db.query(Store).all()

    data = []

    for store in stores:

        reviews = db.query(Review).filter(
            Review.store_id == store.id
        ).count()

        low_reviews = db.query(Review).filter(
            Review.store_id == store.id,
            Review.rating <= 2
        ).count()

        posts = db.query(Post).filter(
            Post.store_id == store.id
        ).count()

        open_tasks = db.query(Task).filter(
            Task.store_id == store.id,
            Task.status == "open"
        ).count()

        data.append({
            "store_id": store.id,
            "store_name": store.name,
            "reviews": reviews,
            "low_reviews": low_reviews,
            "posts": posts,
            "open_tasks": open_tasks
        })

    return data