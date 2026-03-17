from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post

router = APIRouter(prefix="/hq")

templates = Jinja2Templates(directory="app/templates")


@router.get("/scoreboard", response_class=HTMLResponse)
def scoreboard(request: Request, db: Session = Depends(get_db)):

    stores = db.query(Store).all()

    data = []

    for s in stores:

        reviews = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .scalar()
        ) or 0

        posts = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .scalar()
        ) or 0

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text == None)
            .scalar()
        ) or 0

        score = reviews + (posts * 2) - (unreplied * 3)

        data.append({
            "store": s.name,
            "reviews": reviews,
            "posts": posts,
            "unreplied": unreplied,
            "score": score
        })

    data = sorted(data, key=lambda x: x["score"], reverse=True)

    return templates.TemplateResponse(
        "hq_scoreboard.html",
        {
            "request": request,
            "data": data
        }
    )