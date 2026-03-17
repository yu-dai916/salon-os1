from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.task import Task
from app.models.review import Review
from app.models.store import Store
from app.models.post import Post

router = APIRouter(prefix="/store")

templates = Jinja2Templates(directory="app/templates")


@router.get("/{store_id}/page")
def store_dashboard_page(
    store_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    store = db.query(Store).filter(Store.id == store_id).first()

    tasks = (
        db.query(Task)
        .filter(Task.store_id == store_id)
        .filter(Task.status == "open")
        .all()
    )

    reviews = (
        db.query(Review)
        .filter(Review.store_id == store_id)
        .filter(Review.reply_status == "pending")
        .all()
    )

    draft_posts = (
        db.query(Post)
        .filter(Post.store_id == store_id)
        .filter(Post.status == "draft")
        .all()
    )

    return templates.TemplateResponse(
        "store_dashboard.html",
        {
            "request": request,
            "store": store,
            "tasks": tasks,
            "reviews": reviews,
            "draft_posts": draft_posts,
        }
    )