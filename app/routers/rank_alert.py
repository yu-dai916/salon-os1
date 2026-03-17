from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db import get_db
from app.models_meo import KeywordRanking

router = APIRouter(prefix="/rank_alert")


@router.get("/{store_id}")
def rank_alert(store_id: int, db: Session = Depends(get_db)):

    rows = (
        db.query(KeywordRanking)
        .filter(KeywordRanking.store_id == store_id)
        .order_by(desc(KeywordRanking.checked_at))
        .limit(2)
        .all()
    )

    if len(rows) < 2:
        return {"alert": False}

    latest = rows[0]
    prev = rows[1]

    drop = latest.rank - prev.rank

    if drop >= 3:
        return {
            "alert": True,
            "message": f"順位が{drop}位下落しました",
            "previous_rank": prev.rank,
            "current_rank": latest.rank
        }

    return {"alert": False}