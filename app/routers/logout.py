from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/logout")
def logout():
    response = RedirectResponse("/login")
    response.delete_cookie("org_id")
    return response