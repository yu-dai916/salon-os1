import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models_google import GoogleToken
from app.services.google_gbp import (
    build_auth_url,
    exchange_code_for_tokens,
    list_accounts,
)

router = APIRouter(prefix="/google/oauth", tags=["google-oauth"])

DEFAULT_ORG_ID = int(os.getenv("DEFAULT_ORG_ID", "1"))


@router.get("/start")
def oauth_start():
    state = secrets.token_urlsafe(16)
    url = build_auth_url(state=state)
    return {"auth_url": url, "state": state}


@router.get("/callback")
def oauth_callback(code: str | None = None, state: str | None = None, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="missing code")

    tokens = exchange_code_for_tokens(code)

    expires_in = tokens.get("expires_in")
    expires_at = None
    if expires_in is not None:
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))

    org_id = DEFAULT_ORG_ID

    row = db.query(GoogleToken).filter(GoogleToken.org_id == org_id).one_or_none()
    if not row:
        row = GoogleToken(
            org_id=org_id,
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token") or "",
            token_type=tokens.get("token_type"),
            scope=tokens.get("scope"),
            expires_at=expires_at,
        )
        db.add(row)
    else:
        row.access_token = tokens["access_token"]
        if tokens.get("refresh_token"):
            row.refresh_token = tokens["refresh_token"]
        row.token_type = tokens.get("token_type")
        row.scope = tokens.get("scope")
        row.expires_at = expires_at

    db.commit()

    try:
        accounts = list_accounts(row.access_token)
        return {"saved": True, "accounts": accounts}
    except Exception as e:
        return {"saved": True, "accounts_error": str(e)}