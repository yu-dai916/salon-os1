from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/store/mobile/{store_id}", response_class=HTMLResponse)
def store_mobile(store_id: int, request: Request, db: Session = Depends(get_db)):

    store = db.query(Store).filter(Store.id == store_id).first()

    return templates.TemplateResponse(
        "store_mobile.html",
        {
            "request": request,
            "store": store
        }
    )