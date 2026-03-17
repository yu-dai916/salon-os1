from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store

router = APIRouter(prefix="/review")


@router.get("/request/{store_id}")
def review_request(store_id: int, db: Session = Depends(get_db)):

    store = db.query(Store).get(store_id)

    if not store:
        return {"error": "store not found"}

    review_url = f"https://search.google.com/local/writereview?placeid={store.google_place_id}"

    message = f"""
{store.name} にご来店いただきありがとうございました。

よろしければ口コミのご協力をお願いいたします。

↓こちらから投稿できます
{review_url}
"""

    return {
        "store": store.name,
        "review_url": review_url,
        "message": message
    }