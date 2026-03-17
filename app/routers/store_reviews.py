from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.review import Review
from app.models.store import Store
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/store/{store_id}/reviews", response_class=HTMLResponse)
def store_reviews(store_id: int, request: Request, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    reviews = (
        db.query(Review)
        .filter(Review.store_id == store_id)
        .filter(Review.reply_text.is_(None))
        .all()
    )

    return templates.TemplateResponse(
        "store_reviews.html",
        {
            "request": request,
            "store": store,
            "reviews": reviews
        }
    )