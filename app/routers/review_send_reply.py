from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.review import Review
from app.models.task import Task   # ←追加
from app.models.action_log import ActionLog

router = APIRouter(prefix="/reviews")


@router.post("/{review_id}/send_reply")
def send_reply(review_id: int, db: Session = Depends(get_db)):

    review = db.query(Review).filter(Review.id == review_id).first()

    # 既存の返信処理（あるはず）
    review.reply_text = "返信内容"
    db.commit()

    # 🔥 ここ追加
    log = ActionLog(
        store_id=review.store_id,
        user_id=1,  # 今は固定でOK
        action_type="review_reply"
    )

    db.add(log)
    db.commit()

    return {"status": "sent"}