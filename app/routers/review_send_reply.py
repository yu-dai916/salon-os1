from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.review import Review

router = APIRouter(prefix="/reviews")


@router.post("/{review_id}/send_reply")
def send_reply(review_id: int, db: Session = Depends(get_db)):

    review = db.query(Review).get(review_id)

    if not review:
        return {"error": "review not found"}

    # 本番はGoogle APIで返信送信
    review.reply_text = review.reply_draft
    review.reply_status = "sent"

    db.commit()

    return {"review_id": review_id, "status": "sent"}