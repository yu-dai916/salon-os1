from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/hq/demo", response_class=HTMLResponse)
def demo(request: Request):

    return templates.TemplateResponse(
        "hq_demo.html",
        {
            "request": request
        }
    )