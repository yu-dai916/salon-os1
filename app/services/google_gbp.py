import os
import urllib.parse
import requests

GOOGLE_AUTH_BASE = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/business.manage",
    "openid",
    "email",
    "profile",
]


def _require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env var: {name}")
    return v


def build_auth_url(state: str, scopes: list[str] | None = None) -> str:
    client_id = _require_env("GOOGLE_CLIENT_ID")
    redirect_uri = _require_env("GOOGLE_REDIRECT_URI")

    scope = " ".join(scopes or DEFAULT_SCOPES)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "scope": scope,
        "state": state,
    }
    return f"{GOOGLE_AUTH_BASE}?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(code: str) -> dict:
    client_id = _require_env("GOOGLE_CLIENT_ID")
    client_secret = _require_env("GOOGLE_CLIENT_SECRET")
    redirect_uri = _require_env("GOOGLE_REDIRECT_URI")

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=30)

    print("TOKEN REQUEST CLIENT_ID:", client_id, flush=True)
    print("TOKEN REQUEST REDIRECT_URI:", redirect_uri, flush=True)
    print("TOKEN RESPONSE STATUS:", r.status_code, flush=True)
    print("TOKEN RESPONSE BODY:", r.text, flush=True)

    r.raise_for_status()
    return r.json()


def refresh_access_token(refresh_token: str) -> dict:
    client_id = _require_env("GOOGLE_CLIENT_ID")
    client_secret = _require_env("GOOGLE_CLIENT_SECRET")

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    r = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=30)
    if r.status_code >= 400:
        print("REFRESH ERROR:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()


def list_accounts(access_token: str) -> dict:
    url = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code >= 400:
        print("LIST ACCOUNTS ERROR:", r.status_code, r.text)
    r.raise_for_status()
    return r.json()


def create_post(access_token: str, account_name: str, location_name: str, text: str) -> dict:
    """
    account_name 例:
    accounts/16327608271002463532

    location_name 例:
    locations/18316754703303669352
    """
    url = f"https://mybusiness.googleapis.com/v4/{account_name}/{location_name}/localPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "languageCode": "ja",
        "summary": text,
        "topicType": "STANDARD",
    }

    r = requests.post(url, headers=headers, json=data, timeout=30)

    if r.status_code >= 400:
        print("CREATE POST ERROR:", r.status_code, r.text)

    r.raise_for_status()
    return r.json()


def list_locations(access_token: str, account_name: str) -> dict:
    url = f"https://mybusinessbusinessinformation.googleapis.com/v1/{account_name}/locations"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "pageSize": 100,
    }

    r = requests.get(url, headers=headers, params=params, timeout=30)

    if r.status_code >= 400:
        print("LIST LOCATIONS ERROR:", r.status_code, r.text)

    r.raise_for_status()
    return r.json()