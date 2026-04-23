from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta

from app.db import get_db
from app.models.store import Store
from app.models.review import Review

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def calc_review_risk(r):
    score = 0
    text = r.comment or ""

    # ★低評価
    if r.rating and r.rating <= 2:
        score += 40

    # 未返信
    if r.reply_text is None or r.reply_text == "":
        score += 20

    # 直近レビュー
    if r.created_at and r.created_at >= datetime.utcnow() - timedelta(days=7):
        score += 20

    # NGワード
    bad_words = ["最悪", "遅い", "待たされた", "雑", "二度と", "不満"]
    for w in bad_words:
        if w in text:
            score += 30
            break

    # 長文クレーム
    if len(text) > 100:
        score += 20

    # 指名クレーム
    if "藤田" in text:
        score += 20

    return score


@router.get("/store/{store_id}/reviews", response_class=HTMLResponse)
def store_reviews(
    store_id: int,
    request: Request,
    review_id: int = None,
    db: Session = Depends(get_db),
):
    # =========================
    # 店舗取得
    # =========================
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # =========================
    # 未返信口コミ取得（ここが修正ポイント）
    # =========================
    pending_reviews = (
        db.query(Review)
        .filter(Review.store_id == store_id)
        .filter(
            or_(
                Review.reply_text.is_(None),
                Review.reply_text == ""
            )
        )
        .order_by(Review.id.desc())
        .all()
    )

    # =========================
    # リスクスコア付与
    # =========================
    for r in pending_reviews:
        r.risk = calc_review_risk(r)

    # =========================
    # 危険順ソート
    # =========================
    pending_reviews = sorted(
        pending_reviews,
        key=lambda r: r.risk,
        reverse=True
    )

    # =========================
    # 対象口コミ（詳細表示用）
    # =========================
    target_review = None
    if review_id:
        target_review = db.query(Review).filter(Review.id == review_id).first()
        if target_review:
            target_review.risk = calc_review_risk(target_review)

    # =========================
    # レンダリング
    # =========================
    return templates.TemplateResponse(
        "store_reviews.html",
        {
            "request": request,
            "store": store,
            "pending_reviews": pending_reviews,
            "target_review": target_review,
        },
    )