from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import SessionLocal
from app.models import Store, Post, Review
from app.models_metrics import Metric
from app.services.store_score import calc_store_score


def run():

    db: Session = SessionLocal()

    stores = db.query(Store).all()

    for s in stores:

        metric = (
            db.query(Metric)
            .filter(Metric.store_id == s.id)
            .order_by(Metric.metric_date.desc())
            .first()
        )

        rank = None
        clicks = 0
        calls = 0

        if metric:
            rank = metric.google_rank
            clicks = metric.hpb_clicks or 0
            calls = metric.phone_calls or 0

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

        print(f"[store_score] {s.name} score={score}")

    db.close()