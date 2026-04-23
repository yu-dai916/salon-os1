from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.review import Review
from app.services.ai_reply_service import generate_reply_with_strategy

router = APIRouter()


@router.post("/reviews/{review_id}/ai_reply")
def create_ai_reply(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        return {"error": "review not found"}

    strategy, reply = generate_reply_with_strategy(review.comment or "")

    review.reply_draft = reply
    review.reply_strategy = strategy

    db.add(review)
    db.commit()
    db.refresh(review)

    return RedirectResponse(
        url=f"/store/{review.store_id}/reviews",
        status_code=303,
    )


@router.post("/reviews/{review_id}/approve_reply")
def approve_reply(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        return {"error": "review not found"}

    if not review.reply_draft:
        return {"error": "no draft"}

    review.reply_text = review.reply_draft
    review.reply_draft = None
    review.replied_at = datetime.utcnow()

    db.add(review)
    db.commit()
    db.refresh(review)

    return RedirectResponse(
        url=f"/store/{review.store_id}/reviews",
        status_code=303,
    )