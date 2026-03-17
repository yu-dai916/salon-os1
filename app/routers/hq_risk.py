print("🔥 HQRISK FILE EXECUTED 🔥")

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post

router = APIRouter(prefix="/hq")

templates = Jinja2Templates(directory="app/templates")


@router.get("/risk", response_class=HTMLResponse)
def risk_ranking(request: Request, db: Session = Depends(get_db)):

    stores = db.query(Store).all()

    data = []

    for s in stores:

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text == None)
            .scalar()
        ) or 0

        posts = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .scalar()
        ) or 0

        score = 0
        reasons = []

        if unreplied > 0:
            score += unreplied * 10
            reasons.append(f"未返信口コミ {unreplied}")

        if posts == 0:
            score += 30
            reasons.append("投稿なし")

        data.append({
            "store": s,
            "score": score,
            "unreplied": unreplied,
            "posts": posts,
            "reasons": ", ".join(reasons)
        })

    data = sorted(data, key=lambda x: x["score"], reverse=True)
    
    print("DATA LENGTH:", len(data))
    print("DATA:", data)
    return templates.TemplateResponse(
        "hq_risk.html",
        {
            "request": request,
            "data": data
        }
    )