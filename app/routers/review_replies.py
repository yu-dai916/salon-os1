from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.review import Review
from app.services.ai_reply_service import generate_reply

router = APIRouter(prefix="/reviews")


@router.post("/{review_id}/ai_reply")
def create_ai_reply(review_id: int, db: Session = Depends(get_db)):

    review = db.query(Review).get(review_id)

    if not review:
        return {"error": "review not found"}

    reply = generate_reply(review.comment)

    review.reply_draft = reply
    db.commit()

    return {
        "review_id": review_id,
        "reply_draft": reply
    }