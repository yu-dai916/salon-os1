from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db import get_db
from app.models_meo import KeywordRanking

router = APIRouter(prefix="/rank")


@router.get("/{store_id}")
def rank_graph(store_id: int, db: Session = Depends(get_db)):

    rows = (
        db.query(KeywordRanking)
        .filter(KeywordRanking.store_id == store_id)
        .order_by(desc(KeywordRanking.checked_at))
        .limit(30)
        .all()
    )

    return [
        {
            "keyword": r.keyword,
            "rank": r.rank,
            "date": r.checked_at
        }
        for r in rows
    ]