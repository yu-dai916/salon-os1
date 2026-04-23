from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta

from app.db import get_db
from app.models.store import Store
from app.models.post import Post
from app.models.review import Review
from app.models.task import Task
from app.models.action_log import ActionLog

router = APIRouter(prefix="/hq")
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def hq_dashboard(request: Request, db: Session = Depends(get_db)):

    yesterday = datetime.utcnow() - timedelta(days=1)

    stores = db.query(Store).all()

    data = []
    total_impact = 0

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

        unreplied = db.query(Review).filter(
            Review.store_id == store.id,
            or_(
                Review.reply_text.is_(None),
                Review.reply_text == ""
            )
        ).count()

        reply_count = db.query(ActionLog).filter(
            ActionLog.store_id == store.id,
            ActionLog.action_type == "review_reply",
            ActionLog.created_at >= yesterday
        ).count()

        # 🔥 インパクト計算（仮ロジック）
        impact = round(unreplied * 0.3, 1)
        total_impact += impact

        # 🔥 コメント（売れる部分）
        if unreplied >= 5:
            comment = "🚨今すぐ対応しないと機会損失大"
        elif reply_count == 0:
            comment = "⚠昨日未対応（予約減少リスク）"
        elif unreplied >= 1:
            comment = "📋あと少しで改善"
        else:
            comment = "✅良い状態"

        data.append({
            "store_id": store.id,
            "store_name": store.name,
            "reviews": reviews,
            "low_reviews": low_reviews,
            "posts": posts,
            "open_tasks": open_tasks,
            "unreplied": unreplied,
            "reply_count": reply_count,
            "impact": impact,
            "comment": comment
        })

    # 🔥 危険順
    data = sorted(
        data,
        key=lambda x: (x["unreplied"], x["low_reviews"]),
        reverse=True
    )

    return templates.TemplateResponse(
        "hq_dashboard.html",
        {
            "request": request,
            "data": data,
            "total_impact": round(total_impact, 1)
        }
    )