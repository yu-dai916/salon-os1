from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store
from app.models_competitor import Competitor
from app.services.store_ai_diagnosis import analyze_store

router = APIRouter(prefix="/ai")


@router.get("/diagnosis/{store_id}")
def ai_diagnosis(store_id: int, db: Session = Depends(get_db)):

    store = db.query(Store).get(store_id)

    serp = (
        db.query(Competitor)
        .filter(Competitor.keyword == "泉大津 美容室")
        .order_by(Competitor.position)
        .all()
    )

    result = analyze_store(store, serp)

    return {
        "store": store.name,
        "analysis": result
    }