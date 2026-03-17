from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import SessionLocal
from app.models import Store, Post, Review
from app.models_metrics import Metric
from app.services.store_score import calc_store_score

router = APIRouter()

@router.get("/ranking")
def ranking():
    db: Session = SessionLocal()

    stores = db.query(Store).all()
    results = []

    for s in stores:
        metric = (
            db.query(Metric)
            .filter(Metric.store_id == s.id)
            .order_by(Metric.metric_date.desc())
            .first()
        )

        rank = metric.google_rank if metric else None
        clicks = metric.hpb_clicks if metric else None
        calls = metric.phone_calls if metric else None

        posts = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .scalar()
        ) or 0

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text.is_(None))
            .scalar()
        ) or 0

        score = calc_store_score(rank, clicks, calls, posts, unreplied)

        results.append({
            "store": s.name,
            "score": score
        })

    db.close()

    results.sort(key=lambda x: x["score"], reverse=True)
    return results