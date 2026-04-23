from app.db import get_db
from app.models import Store, Post
from app.services.formatter import format_for_google_post
from app.services.line import send_line  # ←これ重要


def run(store_id: int, blog: dict):
    db = next(get_db())

    try:
        store = db.query(Store).filter(Store.id == store_id).first()
        if not store:
            print("STORE NOT FOUND:", store_id)
            return

        print("DEBUG STORE:", store.id, store.area, store.main_menu)

        title = (blog.get("title") or "").strip()
        excerpt = (blog.get("excerpt") or "").strip()
        source_url = (blog.get("url") or "").strip()

        content = format_for_google_post(
            title=title,
            excerpt=excerpt,
            source_url=source_url,
            area=store.area,
            main_menu=store.main_menu,
            store_name=store.name,
            phone_number=store.phone_number,
            cta_url=store.cta_url,
        )

        # -------------------------
        # DB保存
        # -------------------------
        p = Post(
            org_id=store.org_id,
            store_id=store.id,
            status="draft",
            title=title,
            content=content,
            source_title=title or None,
            source_url=source_url,
        )

        db.add(p)
        db.commit()

        print("POST CREATED:", p.id)

        # -------------------------
        # LINE通知（ここが核）
        # -------------------------
        send_line(
            f"""投稿できたで👇

{content}

承認して👇
http://localhost:8000/admin/posts/page
"""
        )

        print("LINE SENT")

    except Exception as e:
        print("AUTO POST ERROR:", e)

    finally:
        db.close()