from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
def login(org_id: int = Form(...)):

    response = RedirectResponse("/hq/page", status_code=303)

    response.set_cookie("org_id", str(org_id))

    return response