from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Store, Post
from app.services.line_notify_service import notify_store_users

router = APIRouter(include_in_schema=True)

templates = Jinja2Templates(directory="app/templates")


# -------------------------
# 投稿承認
# -------------------------
@router.post("/admin/posts/{post_id}/approve")
def approve_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return {"error": "not found"}

    post.status = "approved"

    db.add(post)
    db.commit()

    # 👇ここ追加
    notify_store_users(
        db,
        post.store_id,
        f"【投稿承認】\n{post.content[:20]}"
    )

    return {"status": "approved"}
# -------------------------
# 投稿却下
# -------------------------
@router.post("/admin/posts/{post_id}/reject")
def reject_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return {"error": "not found"}

    post.status = "rejected"
    db.commit()

    return {"status": "rejected"}


# -------------------------
# 投稿一覧API
# -------------------------
@router.get("/admin/posts")
def list_posts(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Post)

    if status:
        query = query.filter(Post.status == status)

    posts = query.order_by(Post.id.desc()).all()

    return [
        {
            "id": p.id,
            "status": p.status,
            "content": p.content,
            "title": p.source_title,
        }
        for p in posts
    ]


# -------------------------
# UIページ
# -------------------------
@router.get("/admin/posts/page", response_class=HTMLResponse)
def posts_page(request: Request):
    return templates.TemplateResponse("posts.html", {"request": request})