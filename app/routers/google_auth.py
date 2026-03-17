from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
import requests

router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8000/google/callback"


@router.get("/google/login")
def google_login():

    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=https://www.googleapis.com/auth/business.manage"
        "&access_type=offline"
        "&prompt=consent"
    )

    return RedirectResponse(url)


@router.get("/google/callback")
def google_callback(code: str):

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    res = requests.post(token_url, data=data)

    token = res.json()

    access_token = token.get("access_token")

    print("ACCESS TOKEN:", access_token)

    return {"google_connected": True}