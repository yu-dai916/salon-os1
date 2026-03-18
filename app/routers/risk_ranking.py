from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post

router = APIRouter(prefix="/hq")
templates = Jinja2Templates(directory="app/templates")


@router.get("/risk", response_class=HTMLResponse)
def risk_ranking(request: Request, db: Session = Depends(get_db)):
    org_id = request.state.user["org_id"]

    stores = db.query(Store).filter(Store.org_id == org_id).all()

    rows = []

    for store in stores:
        low_reviews = db.query(Review).filter(
            Review.store_id == store.id,
            Review.rating <= 2
        ).count()

        unreplied = db.query(Review).filter(
            Review.store_id == store.id,
            Review.reply_text.is_(None)
        ).count()

        posts_count = db.query(Post).filter(
            Post.store_id == store.id
        ).count()

        risk = (low_reviews * 5) + (unreplied * 2) - posts_count

        rows.append({
            "id": store.id,
            "name": store.name,
            "risk": risk,
            "low_reviews": low_reviews,
            "unreplied": unreplied,
            "posts": posts_count,
            "tasks": 0,
        })

    rows.sort(key=lambda x: x["risk"], reverse=True)

    return templates.TemplateResponse(
        "hq_risk.html",
        {
            "request": request,
            "rows": rows
        }
    )