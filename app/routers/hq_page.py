from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post
from app.models.task import Task

router = APIRouter(prefix="/hq")

templates = Jinja2Templates(directory="app/templates")


@router.get("/page")
def hq_page(request: Request, db: Session = Depends(get_db)):

    stores = db.query(Store).all()

    rows = []

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

        rows.append({
            "id": store.id,
            "name": store.name,
            "reviews": reviews,
            "low_reviews": low_reviews,
            "posts": posts,
            "tasks": open_tasks
        })

    return templates.TemplateResponse(
        "hq_dashboard.html",
        {
            "request": request,
            "rows": rows
        }
    )