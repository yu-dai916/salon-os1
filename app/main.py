# =========================
# 基本import
# =========================
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.db import Base, engine, SessionLocal, get_db
from app.db import SessionLocal, get_db

# =========================
# ルーター
# =========================
from app.db import Base, engine, SessionLocal, get_db
from app.models import Store
from app.routers.dashboard import router as dashboard_router
from app.routers.tasks import router as tasks_router
from app.routers.review_replies import router as review_reply_router
from app.routers.tasks_actions import router as tasks_actions_router
from app.routers.review_send_reply import router as send_reply_router
from app.routers.store_dashboard_page import router as store_dashboard_page_router
from app.routers.hq_dashboard import router as hq_router
from app.routers.serp_dashboard import router as serp_router
from app.routers.store_diagnosis import router as diagnosis_router
from app.routers.hq_ranking import router as hq_ranking_router
from app.routers.google_auth import router as google_auth_router
from app.routers.review_request import router as review_request_router
from app.routers.hq_page import router as hq_page_router
from app.routers.rank_graph import router as rank_graph_router
from app.routers.rank_alert import router as rank_alert_router
from app.routers.hq_control import router as hq_control_router
from app.routers.google_locations import router as google_locations_router
from app.routers.hq_demo import router as hq_demo_router
from app.routers.hq_risk_demo import router as risk_demo_router
from app.routers.store_mobile import router as store_mobile_router
from app.routers.risk_ranking import router as risk_router
from app.routers.store_ranking import router as store_ranking_router
from app.routers.login import router as login_router
from app.routers.logout import router as logout_router
from app.routers.store_reviews import router as store_reviews_router
from app.routers.store_posts import router as store_posts_router
from app.routers.task_simple import router as task_simple_router
from app.routers.store_dashboard_test import router as test_router
from app.api.post import router as post_router
from app.api.admin import router as admin_router
from app.routers.hq_dashboard import router as hq_dashboard_router

# =========================
# FastAPI
# =========================
app = FastAPI(title="GBP Platform MVP")

templates = Jinja2Templates(directory="app/templates")

print("🔥 main.py 読まれてる")



# =========================
# ルート
# =========================
@app.get("/")
def root():
    return RedirectResponse("/login")

# =========================
# Router登録
# =========================
app.include_router(dashboard_router)
app.include_router(tasks_router)
app.include_router(review_reply_router)
app.include_router(tasks_actions_router)
app.include_router(send_reply_router)

app.include_router(hq_router)
app.include_router(store_dashboard_page_router)
app.include_router(serp_router)
app.include_router(diagnosis_router)

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

app.include_router(risk_router)
app.include_router(store_ranking_router)
app.include_router(login_router)
app.include_router(logout_router)
app.include_router(store_reviews_router)
app.include_router(store_posts_router)
app.include_router(task_simple_router)
app.include_router(test_router)

app.include_router(post_router)
app.include_router(admin_router)
app.include_router(hq_dashboard_router)
@app.middleware("http")
async def fake_auth(request: Request, call_next):
    path = request.url.path

    # 認証不要
    if (
        path.startswith("/login")
        or path.startswith("/docs")
        or path.startswith("/openapi")
        or path.startswith("/line")
        or path.startswith("/seed")
        or path.startswith("/health")
    ):
        return await call_next(request)

    org_id = request.cookies.get("org_id")

    if not org_id:
        return RedirectResponse("/login")

    request.state.user = {
        "user_id": 1,
        "org_id": int(org_id),
        "role": "HQ_ADMIN",
    }

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

    return await call_next(request)

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
    # 🔥 危険店舗ランキング
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

        if unreplied >= 1:
            score += 30
            reasons.append(f"未返信口コミ {unreplied}")

        if posts_count <= 1:
            score += 20
            reasons.append("投稿少ない")

        if rank is not None and rank > 5:
            score += 20
            reasons.append(f"Google順位 {rank}")

        if clicks is not None and clicks < 30:
            score += 20
            reasons.append("HPBクリック低")

        if score > 0:
            danger_stores.append({
                "store": s.name,
                "score": score,
                "reasons": ", ".join(reasons)
            })

    if not danger_stores:
        danger_stores.append({
            "store": "全店舗",
            "score": 0,
            "reasons": "問題なし（健全）"
        })

    danger_stores = sorted(danger_stores, key=lambda x: x["score"], reverse=True)

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

    # -------------------------
    # return
    # -------------------------
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "stores": stores,
            "posts": posts,
            "store_tasks": store_tasks,
            "danger_stores": danger_stores,
            "unreplied_count": unreplied_count,
            "pending_count": pending_count,
            "inactive_store_count": inactive_store_count,
            "competitor_data": competitor_data,
            "status": status,
            "msg": msg,
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
# 口コミ追加（デモ用）
# -------------------------
@app.post("/reviews")
def create_review(
    store_id: int = Form(...),
    reviewer_name: str = Form(...),
    rating: int = Form(...),
    comment: str = Form(...),
    menu_name: str = Form(""),
    staff_name: str = Form(""),
    db: Session = Depends(get_db),
):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return {"ok": False, "error": "store not found"}

    review = Review(
        store_id=store_id,
        reviewer_name=reviewer_name,
        rating=rating,
        comment=comment,
        menu_name=menu_name,
        staff_name=staff_name,
        reply_text=None,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "ok": True,
        "id": review.id,
        "store_id": review.store_id,
        "reviewer_name": review.reviewer_name,
        "rating": review.rating,
        "comment": review.comment,
    }
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

    notify_store_users(
        db,
        p.store_id,
        f"【投稿承認】\n{p.content[:20]}"
    )

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
# 危険度計算（優先処理版）
# -------------------------
def calc_review_risk(r):
    score = 0
    text = r.comment or ""

    # ① 低評価
    if r.rating and r.rating <= 2:
        score += 40

    # ② 未返信
    if r.reply_text is None:
        score += 20

    # ③ 新しい（7日以内）
    if r.created_at and r.created_at >= datetime.utcnow() - timedelta(days=7):
        score += 20

    # ④ ネガワード
    bad_words = ["最悪", "遅い", "待たされた", "雑", "二度と", "不満"]
    for w in bad_words:
        if w in text:
            score += 30
            break

    # ⑤ 長文
    if len(text) > 100:
        score += 20

    # ⑥ スタッフ名
    if "藤田" in text:
        score += 20

    return score


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
        .all()
    )

    # 🔥 危険度付与
    for r in reviews:
        r.risk = calc_review_risk(r)

    # 🔥 危険度順に並び替え
    reviews = sorted(reviews, key=lambda r: r.risk, reverse=True)

    # 上位10件だけ表示
    reviews = reviews[:10]

    draft_posts = (
        db.query(Post)
        .filter(Post.store_id == store.id)
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
#@app.post("/reviews/{review_id}/ai_reply")
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

    try:
        if not client:
            reply = "（デモ）ご来店ありがとうございます。またお待ちしております。"
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
    except Exception:
        reply = "（デモ）ご来店ありがとうございます。またお待ちしております。"

    # reply_draft が無い環境でも落ちないようにする
    if hasattr(review, "reply_draft"):
        review.reply_draft = reply
    else:
        review.reply_text = reply

    db.add(review)
    db.commit()

    return RedirectResponse(
        url=f"/store/{review.store_id}/reviews",
        status_code=303,
    )

# -------------------------
# 口コミ返信 承認
# -------------------------
#@app.post("/reviews/{review_id}/approve_reply")
def approve_reply(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        return {"error": "review not found"}

    draft = getattr(review, "reply_draft", None)

    if draft:
        review.reply_text = draft
    elif review.reply_text:
        # すでに reply_text に入ってるならそのまま承認扱い
        pass
    else:
        return {"error": "no draft"}

    review.replied_at = datetime.utcnow()

    db.add(review)
    db.commit()

    return RedirectResponse(
        url=f"/store/{review.store_id}/reviews",
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
# Demo seed
# -------------------------
@app.post("/seed/demo")
def seed_demo(db: Session = Depends(get_db)):
    # 既存デモ店舗があれば消す
    demo_codes = ["demo-sakai", "demo-fukai", "demo-otsu"]

    print("Store class:", Store)
    print("Store module:", Store.__module__)
    print("Store attrs:", [c.name for c in Store.__table__.columns])

    existing_stores = (
        db.query(Store)
        .filter(Store.store_code.in_(demo_codes))
        .all()
    )

    existing_store_ids = [s.id for s in existing_stores]
    if existing_store_ids:
        db.query(Review).filter(Review.store_id.in_(existing_store_ids)).delete(synchronize_session=False)
        db.query(Post).filter(Post.store_id.in_(existing_store_ids)).delete(synchronize_session=False)
        db.query(Metric).filter(Metric.store_id.in_(existing_store_ids)).delete(synchronize_session=False)
        db.query(Store).filter(Store.id.in_(existing_store_ids)).delete(synchronize_session=False)
        db.commit()

    # 店舗3件
    s1 = Store(
        org_id=1,
        store_code="demo-sakai",
        name="AVANCE.深井",
        station="深井",
        hpb_url="",
        post_interval_days=2,
        strategy_key="reservation_push",
        phone_number="",
        cta_url=""
    )
    s2 = Store(
        org_id=1,
        store_code="demo-fukai",
        name="アリオ鳳",
        station="鳳",
        hpb_url="",
        post_interval_days=2,
        strategy_key="reservation_push",
        phone_number="",
        cta_url=""
    )
    s3 = Store(
        org_id=1,
        store_code="demo-otsu",
        name="AVANCE.泉大津",
        station="泉大津",
        hpb_url="",
        post_interval_days=2,
        strategy_key="reservation_push",
        phone_number="",
        cta_url=""
    )

    db.add_all([s1, s2, s3])
    db.commit()
    db.refresh(s1)
    db.refresh(s2)
    db.refresh(s3)

    # KPI（店長ページの「今日やること」用）
    m1 = Metric(
        store_id=s1.id,
        metric_date=datetime.utcnow().date(),
        google_rank=14,
        hpb_clicks=11,
        phone_calls=1,
    )
    m2 = Metric(
        store_id=s2.id,
        metric_date=datetime.utcnow().date(),
        google_rank=8,
        hpb_clicks=28,
        phone_calls=4,
    )
    m3 = Metric(
        store_id=s3.id,
        metric_date=datetime.utcnow().date(),
        google_rank=3,
        hpb_clicks=54,
        phone_calls=7,
    )

    db.add_all([m1, m2, m3])

    # 口コミ
    reviews = [
        Review(
            store_id=s1.id,
            reviewer_name="山田花子",
            rating=2,
            comment="カットと髪質改善カラーで来店しましたが、待ち時間が少し長かったです。仕上がりは良かったです。",
            menu_name="カット＋髪質改善カラー",
            staff_name="藤田",
            reply_text=None,
        ),
        Review(
            store_id=s1.id,
            reviewer_name="中村彩",
            rating=5,
            comment="髪質改善トリートメントが良くて手触りがかなり変わりました！",
            menu_name="髪質改善トリートメント",
            staff_name="藤田",
            reply_text=None,
        ),
        Review(
            store_id=s1.id,
            reviewer_name="田中一樹",
            rating=4,
            comment="カットは満足です。またお願いしたいです。",
            menu_name="カット",
            staff_name="藤田",
            reply_text=None,
        ),
        Review(
            store_id=s2.id,
            reviewer_name="松本美咲",
            rating=4,
            comment="ハイライトがきれいで満足です。雰囲気も良かったです。",
            menu_name="カット＋ハイライト",
            staff_name="藤田",
            reply_text=None,
        ),
        Review(
            store_id=s2.id,
            reviewer_name="井上里奈",
            rating=5,
            comment="子連れでも行きやすく、髪質改善カラーの仕上がりも良かったです。",
            menu_name="髪質改善カラー",
            staff_name="藤田",
            reply_text="ご来店ありがとうございました！またお待ちしております。",
        ),
        Review(
            store_id=s3.id,
            reviewer_name="小林舞",
            rating=5,
            comment="カットもカラーも丁寧で安心して任せられました。",
            menu_name="カット＋カラー",
            staff_name="藤田",
            reply_text="ご来店ありがとうございました！またのご来店をお待ちしております。",
        ),
        Review(
            store_id=s3.id,
            reviewer_name="木村愛",
            rating=5,
            comment="髪質改善トリートメントでまとまりが出て大満足です！",
            menu_name="髪質改善トリートメント",
            staff_name="藤田",
            reply_text="嬉しい口コミありがとうございます！またお待ちしております。",
        ),
    ]

    db.add_all(reviews)

    # 投稿（差が出るように店舗ごとに件数を変える）
    posts = [
        Post(
            org_id=1,
            store_id=s2.id,
            status="posted",
            content="春の髪質改善カラー特集を公開しました。",
            source_title="春の髪質改善カラー",
            source_url="",
            posted_at=datetime.utcnow(),
        ),
        Post(
            org_id=1,
            store_id=s2.id,
            status="draft",
            content="顔まわりレイヤーのおすすめスタイル。",
            source_title="顔まわりレイヤー",
            source_url="",
        ),
        Post(
            org_id=1,
            store_id=s3.id,
            status="posted",
            content="髪質改善トリートメントのビフォーアフターを投稿。",
            source_title="髪質改善トリートメント",
            source_url="",
            posted_at=datetime.utcnow(),
        ),
        Post(
            org_id=1,
            store_id=s3.id,
            status="posted",
            content="大人女性向けショート特集を投稿。",
            source_title="大人女性ショート",
            source_url="",
            posted_at=datetime.utcnow(),
        ),
    ]

    db.add_all(posts)
    db.commit()

    return {
        "ok": True,
        "stores": [
            {"id": s1.id, "name": s1.name},
            {"id": s2.id, "name": s2.name},
            {"id": s3.id, "name": s3.name},
        ]
    }
from fastapi import Request
from app.db import SessionLocal
#from app.models.store import Store
from app.models.user import User
from app.models.store_user import StoreUser

# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"ok": True}


@app.post("/line/test")
async def line_test(request: Request):
    body = await request.json()

    events = body.get("events", [])
    if not events:
        return {"ok": True}

    event = events[0]

    user_id = event["source"]["userId"]
    text = event["message"].get("text", "")

    text = text.replace("　", " ").strip()
    text = text.translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    print("📩", user_id, text)

    db = SessionLocal()

    # ユーザー取得 or 作成
    user = db.query(User).filter(
        User.line_user_id == user_id
    ).first()

    if not user:
        user = User(line_user_id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    # =========================
    # 分岐ここから（全部つながる）
    # =========================
    if text == "登録 一覧":
        stores = db.query(Store).all()

        links = db.query(StoreUser).filter(
            StoreUser.user_id == user.id
        ).all()

        my_store_ids = [link.store_id for link in links]

        lines = []
        for store in stores:
            if store.id in my_store_ids:
                lines.append(f"{store.store_code} {store.name}（登録済）")
            else:
                lines.append(f"{store.store_code} {store.name}")

        message = (
            "【店舗一覧】\n"
            + "\n".join(lines)
            + "\n\n登録するには\n「登録 0001」と送信"
        )

        send_line_message(user_id, message)

    elif text.startswith("解除"):
        parts = text.split()

        if len(parts) < 2:
            send_line_message(
                user_id,
                "❌ 店舗コードを入力してください\n例：解除 0001"
            )
            db.close()
            return {"ok": True}

        store_code = parts[1].strip()

        if store_code.isdigit():
            store_code = store_code.zfill(4)

        store = db.query(Store).filter(
            Store.store_code == store_code
        ).first()

        if store:
            link = db.query(StoreUser).filter(
                StoreUser.store_id == store.id,
                StoreUser.user_id == user.id
            ).first()

            if link:
                db.delete(link)
                db.commit()

                send_line_message(
                    user_id,
                    f"❌ 解除完了\n{store.name} を通知対象から外しました"
                )
            else:
                send_line_message(
                    user_id,
                    f"⚠ 未登録です\n{store.name}"
                )
        else:
            send_line_message(
                user_id,
                "❌ 店舗コードが違います\n「登録 一覧」で確認できます"
            )

    elif text.startswith("登録"):
        parts = text.split()

        if len(parts) < 2:
            send_line_message(
                user_id,
                "❌ 店舗コードを入力してください\n例：登録 0001"
            )
            db.close()
            return {"ok": True}

        store_code = parts[1].strip()

        if store_code.isdigit():
            store_code = store_code.zfill(4)

        print("🔥 入力コード =", store_code)

        store = db.query(Store).filter(
            Store.store_code == store_code
        ).first()

        if store:
            exists = db.query(StoreUser).filter(
                StoreUser.store_id == store.id,
                StoreUser.user_id == user.id
            ).first()

            if exists:
                send_line_message(
                    user_id,
                    f"⚠️ すでに登録済み\n{store.name}"
                )
            else:
                link = StoreUser(
                    store_id=store.id,
                    user_id=user.id
                )

                db.add(link)
                db.commit()

                send_line_message(
                    user_id,
                    f"✅ 登録完了\n{store.name} を通知対象にしました"
                )
        else:
            send_line_message(
                user_id,
                f"❌ 店舗コードが違います\n入力コード：{store_code}"
            )

    db.close()
    return {"ok": True}
