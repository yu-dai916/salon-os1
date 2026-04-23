from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.db import get_db
from app.models import Store
from app.models.task import Task
from app.models_metrics import Metric

router = APIRouter(prefix="/store")
templates = Jinja2Templates(directory="app/templates")


@router.get("/{store_id}/page", response_class=HTMLResponse)
def store_dashboard_page(
    store_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    # 👇ここからが関数の中（インデント大事）

    tasks = db.query(Task).filter(
    Task.store_id == store_id,
    Task.type == "review_reply",
    Task.status == "open"
).order_by(
    Task.priority.desc()
).all()

    store = db.query(Store).filter(Store.id == store_id).first()

    if not store:
        return HTMLResponse("store not found", status_code=404)

    metric = (
        db.query(Metric)
        .filter(Metric.store_id == store_id)
        .order_by(Metric.metric_date.desc())
        .first()
    )

    return templates.TemplateResponse("store_dashboard.html", {
        "request": request,
        "store": store,
        "metric": metric,
        "tasks": tasks
    })
    rank = metric.google_rank if metric else None
    clicks = metric.hpb_clicks if metric else None
    calls = metric.phone_calls if metric else None

    sync_tasks(db, store_id)

    tasks = (
        db.query(Task)
        .filter(Task.store_id == store_id)
        .filter(Task.status == "open")
        .all()
    )

    reviews = (
        db.query(Review)
        .filter(Review.store_id == store_id)
        .filter(Review.reply_text.is_(None))
        .order_by(Review.created_at.desc())
        .all()
    )

    draft_posts = (
        db.query(Post)
        .filter(Post.store_id == store_id)
        .order_by(Post.id.desc())
        .all()
    )

    posts_count = (
        db.query(func.count(Post.id))
        .filter(Post.store_id == store_id)
        .scalar()
    ) or 0

    unreplied = (
        db.query(func.count(Review.id))
        .filter(Review.store_id == store_id)
        .filter(Review.reply_text.is_(None))
        .scalar()
    ) or 0

    return templates.TemplateResponse(
        "store_dashboard.html",
        {
            "request": request,
            "store": store,
            "rank": rank,
            "clicks": clicks,
            "calls": calls,
            "posts_count": posts_count,
            "unreplied": unreplied,
            "tasks": tasks,
            "reviews": reviews,
            "draft_posts": draft_posts,
        },
    )