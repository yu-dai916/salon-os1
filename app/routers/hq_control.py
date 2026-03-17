from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post
from app.models_metrics import Metric

from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/hq")
templates = Jinja2Templates(directory="app/templates")


@router.get("/control", response_class=HTMLResponse)
def hq_control(request: Request, db: Session = Depends(get_db)):

    stores = db.query(Store).all()

    rows = []

    for s in stores:

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text.is_(None))
            .scalar()
        ) or 0

        drafts = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .filter(Post.status == "draft")
            .scalar()
        ) or 0

        metric = (
            db.query(Metric)
            .filter(Metric.store_id == s.id)
            .order_by(Metric.metric_date.desc())
            .first()
        )

        rank = metric.google_rank if metric else None

        # 状態判定
        status = "🟢"

        if unreplied > 3:
            status = "🔴"
        elif unreplied > 0 or (rank and rank > 10):
            status = "🟡"

        rows.append({
            "store_id": s.id,
            "store": s.name,
            "status": status,
            "unreplied": unreplied,
            "drafts": drafts,
            "rank": rank
        })

    return templates.TemplateResponse(
        "hq_control.html",
        {
            "request": request,
            "rows": rows
        }
    )