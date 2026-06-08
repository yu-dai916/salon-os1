from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.store import Store
from app.models.review import Review
from app.models.post import Post

router = APIRouter(prefix="/hq")
templates = Jinja2Templates(directory="app/templates")


@router.get("/risk", response_class=HTMLResponse)
def risk_ranking(request: Request, db: Session = Depends(get_db)):
    print("🔥 RISK ROUTE 動いてる")

    stores = db.query(Store).all()
    rows = []

    for store in stores:
        low_reviews = db.query(Review).filter(
            Review.store_id == store.id,
            Review.rating <= 2
        ).count()

        unreplied = db.query(Review).filter(
            Review.store_id == store.id,
            Review.reply_text.is_(None)
        ).count()

        posts_count = db.query(Post).filter(
            Post.store_id == store.id
        ).count()

        # -------------------------
        # リスクスコア（シンプル設計）
        # -------------------------
        risk = 0

        if low_reviews > 0:
            risk += low_reviews * 10

        if unreplied > 0:
            risk += unreplied * 5

        if posts_count == 0:
            risk += 10

        # -------------------------
        # やること（最重要）
        # -------------------------
        tasks = []

        if unreplied > 0:
            tasks.append(f"未返信口コミ {unreplied}件 → 今日中に返信")

        if low_reviews > 0:
            tasks.append(f"低評価 {low_reviews}件 → 内容確認")

        if posts_count == 0:
            tasks.append("投稿なし → 今週2件投稿")

        if not tasks:
            tasks.append("問題なし（このまま維持）")

        # -------------------------
        # rowsに追加
        # -------------------------
        rows.append({
            "id": store.id,
            "name": store.name,
            "risk": risk,
            "low_reviews": low_reviews,
            "unreplied": unreplied,
            "posts": posts_count,
            "tasks": tasks,
        })

    # リスク高い順
    rows.sort(key=lambda x: x["risk"], reverse=True)

    return templates.TemplateResponse(
        "hq_risk.html",
        {
            "request": request,
            "rows": rows
        }
    )