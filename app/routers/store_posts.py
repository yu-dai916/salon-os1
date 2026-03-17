from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store
from app.models.post import Post

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/store/{store_id}/posts", response_class=HTMLResponse)
def store_posts(store_id: int, request: Request, db: Session = Depends(get_db)):

    store = db.query(Store).filter(Store.id == store_id).first()

    draft_posts = (
        db.query(Post)
        .filter(Post.store_id == store_id)
        .order_by(Post.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        "store_posts.html",
        {
            "request": request,
            "store": store,
            "draft_posts": draft_posts
        }
    )