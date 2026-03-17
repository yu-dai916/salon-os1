from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post
from app.models_competitor import Competitor
from app.services.store_diagnosis import diagnose

router = APIRouter(prefix="/analysis")


@router.get("/{store_id}")
def store_analysis(store_id: int, db: Session = Depends(get_db)):

    store = db.query(Store).get(store_id)

    serp = (
        db.query(Competitor)
        .filter(Competitor.keyword == "泉大津 美容室")
        .order_by(Competitor.position)
        .all()
    )

    store_reviews = db.query(Review).filter(
        Review.store_id == store_id
    ).count()

    last7 = datetime.utcnow() - timedelta(days=7)

    store_posts_last7 = db.query(Post).filter(
        Post.store_id == store_id,
        Post.created_at >= last7
    ).count()

    result = diagnose(store, serp, store_reviews, store_posts_last7)

    return {
        "store": store.name,
        "analysis": result
    }