from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Org

router = APIRouter()

@router.post("/login")
def login(
    org_code:str = Form(...),
    db:Session = Depends(get_db)
):

    org = db.query(Org).filter(Org.code == org_code).first()

    if not org:
        return {"error":"org not found"}

    res = RedirectResponse("/", status_code=303)
    res.set_cookie("org_id", str(org.id))

    return res