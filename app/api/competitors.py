from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models_competitor import Competitor

router = APIRouter(prefix="/competitors")


@router.get("/")
def list_competitors(db: Session = Depends(get_db)):

    rows = db.query(Competitor).all()

    return [
        {
            "store_id": r.store_id,
            "name": r.name,
            "keyword": r.keyword
        }
        for r in rows
    ]