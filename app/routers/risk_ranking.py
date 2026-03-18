from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post
from app.models.task import Task

router = APIRouter(prefix="/hq")
templates = Jinja2Templates(directory="app/templates")


@router.get("/risk", response_class=HTMLResponse)
def risk_ranking(request: Request, db: Session = Depends(get_db)):
    org_id = request.state.user["org_id"]

    stores = db.query(Store).filter(Store.org_id == org_id).all()

    rows = []

    for store in stores:
        # 低評価レビュー
        low_reviews = db.query(Review).filter(
            Review.store_id == store.id,
            Review.rating <= 2
        ).count()

        # 未返信口コミ
        unreplied = db.query(Review).filter(
            Review.store_id == store.id,
            Review.reply_text.is_(None)
        ).count()

        # 直近7日以内の投稿
        recent_posts = db.query(Post).filter(
            Post.store_id == store.id,
            Post.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()

        # 未対応タスク
        open_tasks = db.query(Task).filter(
            Task.store_id == store.id,
            Task.status == "open"
        ).count()

        # リスクスコア
        risk = (
            low_reviews * 5 +
            unreplied * 2 +
            open_tasks * 1 -
            recent_posts * 2
        )

        rows.append({
            "id": store.id,
            "name": store.name,
            "risk": risk,
            "low_reviews": low_reviews,
            "unreplied": unreplied,
            "posts": recent_posts,
            "tasks": open_tasks
        })

    rows.sort(key=lambda x: x["risk"], reverse=True)

    return templates.TemplateResponse(
        "hq_risk.html",
        {
            "request": request,
            "rows": rows
        }
    )