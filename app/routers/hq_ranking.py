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


@router.get("/ranking", response_class=HTMLResponse)
def hq_ranking(request: Request, db: Session = Depends(get_db)):
    org_id = request.state.user["org_id"]

    stores = db.query(Store).filter(Store.org_id == org_id).all()

    rows = []

    for store in stores:
        review_count = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == store.id)
            .scalar()
        ) or 0

        posted_count = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == store.id)
            .filter(Post.status == "posted")
            .scalar()
        ) or 0

        score = review_count * 2 + posted_count * 5

        rows.append({
            "id": store.id,
            "name": store.name,
            "review_count": review_count,
            "posted_count": posted_count,
            "score": score,
        })

    rows.sort(key=lambda x: x["score"], reverse=True)

    return templates.TemplateResponse(
        "hq_ranking.html",
        {
            "request": request,
            "rows": rows
        }
    )