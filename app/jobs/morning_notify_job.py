import random
from datetime import datetime, timezone

from app.db import SessionLocal
from app.models.review import Review
from app.models.task import Task
from app.models.store import Store
from app.models.store_user import StoreUser
from app.models.user import User

from app.services.line_push import send_line


def run():
    print("🔥 MORNING START")

    db = SessionLocal()
    stores = db.query(Store).all()

    for store in stores:
        print(f"\n--- STORE {store.id} {store.name} ---")

        # =========================
        # ① 今日送信済みチェック
        # =========================
        today = datetime.now(timezone.utc).date()
        start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)

        already_sent = db.query(Task).filter(
            Task.store_id == store.id,
            Task.title == "morning_sent",
            Task.created_at >= start
        ).first()

        print("already_sent:", already_sent)

        if already_sent:
            print("⏩ skip: already sent")
            continue

        # =========================
        # ② 紐付けユーザー取得
        # =========================
        links = db.query(StoreUser).filter(
            StoreUser.store_id == store.id
        ).all()

        print("links:", links)

        if not links:
            print("⏩ skip: no linked users")
            continue

        # =========================
        # ③ 未返信口コミ数
        # =========================
        unreplied = db.query(Review).filter(
            Review.store_id == store.id,
            Review.reply_text.is_(None)
        ).count()

        print("unreplied:", unreplied)

        # 🔥 未返信ないなら送らない
        if unreplied == 0:
            print("⏩ skip: no unreplied reviews")
            continue

        # =========================
        # ④ 通知文（強化版）
        # =========================
        text = f"""【{store.name}】

未返信口コミ：{unreplied}件

本部でも確認しています

このまま放置すると
新規のお客様が他店に流れます

■今やること（3分）
・口コミ返信 {unreplied}件

👇ここから対応
http://localhost:8000/store/{store.id}/reviews

■完了すると
→ 今日の予約＋1件見込み
"""

        # =========================
        # ⑤ 送信（重複防止）
        # =========================
        sent_users = set()

        for link in links:
            user = db.query(User).filter(
                User.id == link.user_id
            ).first()

            print("👤 user:", user)
            print("📱 line_user_id:", user.line_user_id if user else None)

            if not user or not user.line_user_id:
                print("⏩ skip: invalid user")
                continue

            if user.line_user_id in sent_users:
                print("⏩ skip: duplicate user")
                continue

            print("📨 sending LINE to:", user.line_user_id)
            send_line(user.line_user_id, text)

            sent_users.add(user.line_user_id)

        # =========================
        # ⑥ 送信ログ保存
        # =========================
        log = Task(
            store_id=store.id,
            title="morning_sent",
            status="done"
        )
        db.add(log)
        db.commit()

        print("✅ sent & logged")

    db.close()
    print("🔥 MORNING END")