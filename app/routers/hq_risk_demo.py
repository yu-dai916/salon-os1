from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/hq/risk_demo", response_class=HTMLResponse)
def risk_demo(request: Request):

    return templates.TemplateResponse(
        "hq_risk_demo.html",
        {
            "request": request
        }
    )