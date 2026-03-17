import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

from openai import OpenAI

from app.db import Base, engine, get_db
from app.models import Org, Store, Post, Review
from app.models_metrics import Metric
from app.models_competitor import Competitor
from app.models_keywords import Keyword, StoreKeyword
from app.models_agency import Agency
from app.models_meo import KeywordRanking, CompetitorMetric

from app.services.hpb import fetch_latest_blog
from app.services.formatter import format_for_google_post
from app.services.store_ai_analyzer import analyze_store
from app.services.store_task_generator import generate_tasks
from app.services.google_competitors import get_google_competitors

from app.routers.dashboard import router as dashboard_router
from app.routers.tasks import router as tasks_router
from app.routers.replies import router as ai_router
from app.routers.review_replies import router as review_reply_router
from app.routers.tasks_actions import router as tasks_actions_router
from app.routers.review_send_reply import router as send_reply_router
from app.routers.hq_dashboard import router as hq_router
from app.routers.store_dashboard_page import router as store_dashboard_page_router
from app.routers.hq_dashboard import router as hq_router
from app.routers.serp_dashboard import router as serp_router
from app.routers.ai_store_diagnosis import router as ai_diagnosis_router
from app.routers.store_diagnosis import router as diagnosis_router
from app.routers.risk_ranking import router as risk_router
from app.routers.review_request import router as review_request_router
from app.routers.hq_page import router as hq_page_router
from app.routers.hq_ranking import router as hq_ranking_router
from app.routers.google_auth import router as google_auth_router
from app.routers.rank_graph import router as rank_graph_router
from app.routers.rank_alert import router as rank_alert_router
from app.routers.hq_control import router as hq_control_router
from app.routers.google_locations import router as google_locations_router
from app.routers.hq_demo import router as hq_demo_router
from app.routers.hq_risk_demo import router as risk_demo_router
from app.routers.store_mobile import router as store_mobile_router
from app.routers.hq_risk import router as hq_risk_router
from app.routers.store_ranking import router as store_ranking_router
from app.routers.login import router as login_router
from app.routers.logout import router as logout_router
from app.routers.store_reviews import router as store_reviews_router
from app.routers.store_posts import router as store_posts_router
from app.routers.review_quick_reply import router as quick_reply_router

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# まず FastAPI を作る
app = FastAPI(title="GBP Platform MVP")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def root():
    return RedirectResponse("/login")
# その後 router を登録
app.include_router(dashboard_router)
app.include_router(tasks_router)
app.include_router(ai_router)
app.include_router(review_reply_router)
app.include_router(tasks_actions_router)
app.include_router(send_reply_router)

app.include_router(hq_router)

app.include_router(store_dashboard_page_router)

app.include_router(serp_router)
app.include_router(ai_diagnosis_router)
app.include_router(diagnosis_router)

# 危険店舗ランキング
app.include_router(hq_ranking_router)
app.include_router(google_auth_router)

app.include_router(review_request_router)
app.include_router(hq_page_router)
app.include_router(rank_graph_router)
app.include_router(rank_alert_router)
app.include_router(hq_control_router)
app.include_router(google_locations_router)
app.include_router(hq_demo_router)
app.include_router(risk_demo_router)
app.include_router(store_mobile_router)
app.include_router(hq_risk_router)
app.include_router(store_ranking_router)
app.include_router(login_router)
app.include_router(logout_router)
app.include_router(store_reviews_router)
app.include_router(store_posts_router)
app.include_router(quick_reply_router)
# fake auth
# -------------------------
# -------------------------
# auth middleware
# -------------------------
@app.middleware("http")
async def fake_auth(request: Request, call_next):

    path = request.url.path

    # loginとdocsはスルー
    if path.startswith("/login") or path.startswith("/docs") or path.startswith("/openapi"):
        return await call_next(request)

    org_id = request.cookies.get("org_id")

    # 未ログイン
    if not org_id:
        return RedirectResponse("/login")

    request.state.user = {
        "user_id": 1,
        "org_id": int(org_id),
        "role": "HQ_ADMIN"
    }

    response = await call_next(request)

    return response

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def _org_id(request: Request):
    return int(getattr(request.state, "user", {}).get("org_id", 1))


# -------------------------
# Dashboard
# -------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    status: str = "all",
    msg: str = "",
    db: Session = Depends(get_db),
):
    org_id = _org_id(request)

    stores = db.query(Store).filter(Store.org_id == org_id).all()

    # -------------------------
    # store keywords
    # -------------------------
    store_keywords_map = {}

    keyword_rows = (
        db.query(StoreKeyword, Keyword)
        .join(Keyword, Keyword.id == StoreKeyword.keyword_id)
        .order_by(StoreKeyword.priority.asc())
        .all()
    )

    for sk, k in keyword_rows:
        store_keywords_map.setdefault(sk.store_id, []).append({
            "keyword": k.keyword,
            "priority": sk.priority,
        })

    competitors = (
        db.query(Competitor)
        .filter(Competitor.org_id == org_id)
        .all()
    )

    metrics = (
        db.query(
            Store.name,
            Metric.google_rank,
            Metric.hpb_clicks,
            Metric.phone_calls
        )
        .join(Store, Store.id == Metric.store_id)
        .order_by(Metric.metric_date.desc())
        .limit(20)
        .all()
    )

    # -------------------------
    # posts
    # -------------------------
    post_query = (
        db.query(Post)
        .filter(Post.org_id == org_id)
        .order_by(Post.id.desc())
    )

    if status != "all":
        post_query = post_query.filter(Post.status == status)

    posts = post_query.limit(50).all()

    # -------------------------
    # summary counts
    # -------------------------
    unreplied_count = (
        db.query(func.count(Review.id))
        .join(Store, Store.id == Review.store_id)
        .filter(Store.org_id == org_id)
        .filter(Review.reply_text.is_(None))
        .scalar()
    ) or 0

    pending_count = (
        db.query(func.count(Post.id))
        .filter(Post.org_id == org_id)
        .filter(Post.status == "draft")
        .scalar()
    ) or 0

    inactive_store_count = 0
    for s in stores:
        posted_count = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .filter(Post.status == "posted")
            .scalar()
        ) or 0

        if posted_count == 0:
            inactive_store_count += 1

    # -------------------------
    # AI advice
    # -------------------------
    ai_advice = []

    for s in stores:
        metric = (
            db.query(Metric)
            .filter(Metric.store_id == s.id)
            .order_by(Metric.metric_date.desc())
            .first()
        )

        rank = metric.google_rank if metric else None
        clicks = metric.hpb_clicks if metric else None
        calls = metric.phone_calls if metric else None

        posts_count = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .scalar()
        ) or 0

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text.is_(None))
            .scalar()
        ) or 0

        advice = analyze_store(rank, clicks, calls, posts_count, unreplied)

        ai_advice.append({
            "store": s.name,
            "advice": advice
        })

    # -------------------------
    # 今週の集客タスク
    # -------------------------
    store_tasks = []

    for s in stores:
        metric = (
            db.query(Metric)
            .filter(Metric.store_id == s.id)
            .order_by(Metric.metric_date.desc())
            .first()
        )

        rank = metric.google_rank if metric else None
        clicks = metric.hpb_clicks if metric else None
        calls = metric.phone_calls if metric else None

        posts_count = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .filter(Post.status == "posted")
            .scalar()
        ) or 0

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text.is_(None))
            .scalar()
        ) or 0

        tasks = generate_tasks(rank, clicks, calls, posts_count, unreplied)

        store_tasks.append({
            "store": s.name,
            "tasks": tasks
        })

    # -------------------------
    # 危険店舗ランキング
    # -------------------------
    danger_stores = []

    for s in stores:
        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id == s.id)
            .filter(Review.reply_text.is_(None))
            .scalar()
        ) or 0

        posts_count = (
            db.query(func.count(Post.id))
            .filter(Post.store_id == s.id)
            .filter(Post.status == "posted")
            .scalar()
        ) or 0

        metric = (
            db.query(Metric)
            .filter(Metric.store_id == s.id)
            .order_by(Metric.metric_date.desc())
            .first()
        )

        rank = metric.google_rank if metric else None
        clicks = metric.hpb_clicks if metric else None

        score = 0
        reasons = []

        if unreplied > 3:
            score += 40
            reasons.append(f"未返信口コミ {unreplied}")

        if posts_count == 0:
            score += 20
            reasons.append("投稿なし")

        if rank is not None and rank > 10:
            score += 20
            reasons.append(f"Google順位 {rank}")

        if clicks is not None and clicks < 20:
            score += 20
            reasons.append("HPBクリック低")

        danger_stores.append({
            "store": s.name,
            "score": score,
            "reasons": ", ".join(reasons)
        })

    danger_stores = sorted(danger_stores, key=lambda x: x["score"], reverse=True)

    # -------------------------
    # pending_map
    # -------------------------
    pending_rows = (
        db.query(
            Post.store_id,
            func.count(Post.id)
        )
        .filter(Post.org_id == org_id)
        .filter(Post.status == "draft")
        .group_by(Post.store_id)
        .all()
    )

    pending_map = {store_id: count for store_id, count in pending_rows}

    # -------------------------
    # competitor_data
    # -------------------------
    competitor_data = []

    for s in stores:
        if s.station:
            keyword = f"{s.station.replace('駅', '').strip()} 美容室"
        else:
            keyword = "美容室"

        try:
            data = get_google_competitors(keyword)
        except Exception:
            data = []

        competitor_data.append({
            "store": s.name,
            "keyword": keyword,
            "results": data[:5],
        })

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "stores": stores,
            "posts": posts,
            "competitors": competitors,
            "metrics": metrics,
            "ai_advice": ai_advice,
            "store_tasks": store_tasks,
            "danger_stores": danger_stores,
            "unreplied_count": unreplied_count,
            "pending_count": pending_count,
            "inactive_store_count": inactive_store_count,
            "pending_map": pending_map,
            "warn_pending": 30,
            "max_pending": 50,
            "status": status,
            "msg": msg,
            "store_keywords_map": store_keywords_map,
            "competitor_data": competitor_data,
        },
    )

# -------------------------
# 店舗追加
# -------------------------
@app.post("/stores")
def create_store(
    request: Request,
    store_code: str = Form(...),
    name: str = Form(...),
    station: str = Form(None),
    hpb_url: str = Form(None),
    post_interval_days: int = Form(2),
    strategy_key: str = Form("reservation_push"),
    phone_number: str = Form(None),
    cta_url: str = Form(None),
    db: Session = Depends(get_db),
):
    org_id = _org_id(request)

    store = Store(
        org_id=org_id,
        store_code=store_code,
        name=name,
        station=station,
        hpb_url=hpb_url,
        post_interval_days=post_interval_days,
        strategy_key=strategy_key,
        phone_number=phone_number,
        cta_url=cta_url,
    )

    db.add(store)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return RedirectResponse(url="/?msg=store_duplicate", status_code=303)

    return RedirectResponse(url="/?msg=created", status_code=303)


# -------------------------
# HPBブログ取得
# -------------------------
@app.post("/stores/{store_id}/fetch_hpb")
def fetch_hpb(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()

    if not store:
        return JSONResponse({"ok": False})

    data = fetch_latest_blog(store.hpb_url)

    content = format_for_google_post(
        data.get("title"),
        data.get("excerpt"),
        data.get("url")
    )

    p = Post(
        org_id=store.org_id,
        store_id=store.id,
        status="draft",
        content=content,
        source_title=data.get("title"),
        source_url=data.get("url"),
    )

    db.add(p)
    db.commit()

    return RedirectResponse(url="/?msg=created", status_code=303)


# -------------------------
# 投稿承認
# -------------------------
@app.post("/posts/{post_id}/approve")
def approve_post(post_id: int, db: Session = Depends(get_db)):
    p = db.query(Post).filter(Post.id == post_id).first()

    if not p:
        return {"error": "not found"}

    p.status = "posted"
    p.posted_at = datetime.utcnow()

    db.add(p)
    db.commit()

    return RedirectResponse(url="/?msg=approved", status_code=303)


# -------------------------
# 投稿拒否
# -------------------------
@app.post("/posts/{post_id}/reject")
def reject_post(post_id: int, db: Session = Depends(get_db)):
    p = db.query(Post).filter(Post.id == post_id).first()

    if not p:
        return {"error": "not found"}

    p.status = "rejected"

    db.add(p)
    db.commit()

    return RedirectResponse(url="/?msg=rejected", status_code=303)


# -------------------------
# キーワード一覧
# -------------------------
@app.get("/keywords")
def list_keywords(request: Request, db: Session = Depends(get_db)):
    org_id = _org_id(request)

    rows = (
        db.query(Keyword)
        .filter(Keyword.org_id == org_id)
        .order_by(Keyword.id.desc())
        .all()
    )

    return [
        {
            "id": k.id,
            "keyword": k.keyword,
            "category": k.category,
            "is_active": k.is_active,
        }
        for k in rows
    ]


# -------------------------
# キーワード追加
# -------------------------
@app.post("/keywords")
def create_keyword(
    request: Request,
    keyword: str = Form(...),
    category: str = Form("custom"),
    db: Session = Depends(get_db),
):
    org_id = _org_id(request)

    row = Keyword(
        org_id=org_id,
        keyword=keyword.strip(),
        category=category,
        is_active=True,
    )

    db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except IntegrityError:
        db.rollback()
        return {"ok": False, "error": "duplicate keyword"}

    return {"ok": True, "id": row.id, "keyword": row.keyword}


# -------------------------
# 店舗にキーワード割当
# -------------------------
@app.post("/stores/{store_id}/keywords")
def assign_keyword_to_store(
    store_id: int,
    keyword_id: int = Form(...),
    priority: int = Form(1),
    db: Session = Depends(get_db),
):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return {"ok": False, "error": "store not found"}

    keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
    if not keyword:
        return {"ok": False, "error": "keyword not found"}

    row = StoreKeyword(
        store_id=store_id,
        keyword_id=keyword_id,
        priority=priority,
        is_active=True,
    )

    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"ok": False, "error": "already assigned"}

    return {"ok": True}


# -------------------------
# 店舗ごとのキーワード一覧
# -------------------------
@app.get("/stores/{store_id}/keywords")
def list_store_keywords(store_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(StoreKeyword, Keyword)
        .join(Keyword, Keyword.id == StoreKeyword.keyword_id)
        .filter(StoreKeyword.store_id == store_id)
        .order_by(StoreKeyword.priority.asc(), StoreKeyword.id.asc())
        .all()
    )

    return [
        {
            "store_keyword_id": sk.id,
            "keyword_id": k.id,
            "keyword": k.keyword,
            "priority": sk.priority,
            "is_active": sk.is_active,
            "category": k.category,
        }
        for sk, k in rows
    ]


# -------------------------
# Agency追加
# -------------------------
@app.post("/agencies")
def create_agency(name: str = Form(...), db: Session = Depends(get_db)):
    row = Agency(name=name.strip())
    db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except IntegrityError:
        db.rollback()
        return {"ok": False, "error": "duplicate agency"}

    return {"ok": True, "id": row.id, "name": row.name}


# -------------------------
# Agency一覧
# -------------------------
@app.get("/agencies")
def list_agencies(db: Session = Depends(get_db)):
    rows = db.query(Agency).order_by(Agency.id.desc()).all()
    return [{"id": a.id, "name": a.name} for a in rows]


# -------------------------
# Agencyダッシュボード
# -------------------------
@app.get("/agency_dashboard")
def agency_dashboard(db: Session = Depends(get_db)):
    agencies = db.query(Agency).all()
    result = []

    for a in agencies:
        org_ids = [o.id for o in db.query(Org).filter(Org.agency_id == a.id).all()]
        store_ids = [s.id for s in db.query(Store).filter(Store.org_id.in_(org_ids)).all()]

        unreplied = (
            db.query(func.count(Review.id))
            .filter(Review.store_id.in_(store_ids))
            .filter(Review.reply_text.is_(None))
            .scalar()
        ) or 0

        pending_posts = (
            db.query(func.count(Post.id))
            .filter(Post.store_id.in_(store_ids))
            .filter(Post.status == "draft")
            .scalar()
        ) or 0

        result.append({
            "agency": a.name,
            "org_count": len(org_ids),
            "store_count": len(store_ids),
            "unreplied_reviews": unreplied,
            "pending_posts": pending_posts,
        })

    return result


# -------------------------
# 店長ダッシュボード
# -------------------------
@app.get("/store_dashboard/{store_id}", response_class=HTMLResponse)
def store_dashboard(store_id: int, request: Request, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return HTMLResponse("store not found", status_code=404)

    metric = (
        db.query(Metric)
        .filter(Metric.store_id == store.id)
        .order_by(Metric.metric_date.desc())
        .first()
    )

    rank = metric.google_rank if metric else None
    clicks = metric.hpb_clicks if metric else None
    calls = metric.phone_calls if metric else None

    posts_count = (
        db.query(func.count(Post.id))
        .filter(Post.store_id == store.id)
        .filter(Post.status == "posted")
        .scalar()
    ) or 0

    unreplied = (
        db.query(func.count(Review.id))
        .filter(Review.store_id == store.id)
        .filter(Review.reply_text.is_(None))
        .scalar()
    ) or 0

    tasks = generate_tasks(rank, clicks, calls, posts_count, unreplied)

    reviews = (
        db.query(Review)
        .filter(Review.store_id == store.id)
        .filter(Review.reply_text.is_(None))
        .order_by(Review.id.desc())
        .limit(10)
        .all()
    )

    draft_posts = (
        db.query(Post)
        .filter(Post.store_id == store.id)
        .filter(Post.status == "draft")
        .order_by(Post.id.desc())
        .limit(10)
        .all()
    )

    return templates.TemplateResponse(
        "store_dashboard.html",
        {
            "request": request,
            "store": store,
            "tasks": tasks,
            "reviews": reviews,
            "draft_posts": draft_posts,
            "rank": rank,
            "clicks": clicks,
            "calls": calls,
            "posts_count": posts_count,
            "unreplied": unreplied,
        },
    )


# -------------------------
# AI口コミ返信
# -------------------------
@app.post("/reviews/{review_id}/ai_reply")
def ai_reply(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        return {"error": "review not found"}

    prompt = f"""
美容室のGoogle口コミ返信を書いてください

口コミ:
{review.comment or ""}

条件
・丁寧
・来店感謝
・次回来店導線
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content

    review.reply_draft = reply
    db.add(review)
    db.commit()

    return RedirectResponse(
        url=f"/store_dashboard/{review.store_id}",
        status_code=303,
    )


# -------------------------
# 口コミ返信 承認
# -------------------------
@app.post("/reviews/{review_id}/approve_reply")
def approve_reply(review_id: int, db: Session = Depends(get_db)):

    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        return {"error": "review not found"}

    if not review.reply_draft:
        return {"error": "no draft"}

    review.reply_text = review.reply_draft
    review.replied_at = datetime.utcnow()

    db.add(review)
    db.commit()

    return RedirectResponse(
        url=f"/store_dashboard/{review.store_id}",
        status_code=303,
    )

# -------------------------
# 店舗KPI
# -------------------------
@app.get("/store_metrics/{store_id}")
def store_metrics(store_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(Metric)
        .filter(Metric.store_id == store_id)
        .order_by(Metric.metric_date.desc())
        .limit(30)
        .all()
    )

    return [
        {
            "id": r.id,
            "store_id": r.store_id,
            "metric_date": r.metric_date,
            "google_rank": r.google_rank,
            "hpb_clicks": r.hpb_clicks,
            "phone_calls": r.phone_calls,
        }
        for r in rows
    ]
@app.get("/competitors")
def competitors(keyword: str):
    data = get_google_competitors(keyword)
    return data

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"ok": True}