from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app.db import get_db
from app.models_competitor import Competitor

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/serp")
def serp_dashboard(request: Request, db: Session = Depends(get_db)):

    rows = (
        db.query(Competitor)
        .filter(Competitor.keyword == "泉大津 美容室")
        .order_by(Competitor.position)
        .all()
    )

    return templates.TemplateResponse(
        "serp_dashboard.html",
        {
            "request": request,
            "rows": rows
        }
    )