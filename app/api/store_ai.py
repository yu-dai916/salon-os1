from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import SessionLocal
from app.models import Store, Post, Review
from app.models_metrics import Metric
from app.services.store_ai_analyzer import analyze_store

router = APIRouter()

@router.get("/store-ai/{store_id}")
def store_ai(store_id:int):

    db: Session = SessionLocal()

    s = db.query(Store).filter(Store.id == store_id).first()

    metric = (
        db.query(Metric)
        .filter(Metric.store_id == store_id)
        .order_by(Metric.metric_date.desc())
        .first()
    )

    rank = metric.google_rank if metric else None
    clicks = metric.hpb_clicks if metric else None
    calls = metric.phone_calls if metric else None

    posts = (
        db.query(func.count(Post.id))
        .filter(Post.store_id == store_id)
        .scalar()
    )

    unreplied = (
        db.query(func.count(Review.id))
        .filter(Review.store_id == store_id)
        .filter(Review.reply_text.is_(None))
        .scalar()
    )

    advice = analyze_store(rank, clicks, calls, posts, unreplied)

    db.close()

    return {
        "store": s.name,
        "advice": advice
    }