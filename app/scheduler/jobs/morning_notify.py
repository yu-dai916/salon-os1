import requests
import os
import random
from datetime import datetime, timezone, timedelta

from sqlalchemy import func

from app.db import SessionLocal
from app.models.review import Review
from app.models.task import Task
from app.models.store import Store
from app.models.post import Post
from app.models.store_user import StoreUser
from app.models.user import User
from app.models.action_log import ActionLog

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")


def send(user_id, text):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}]
    }

    requests.post(url, headers=headers, json=data)


def run():

    print("🔥 MORNING START")

    now = datetime.now()

    # 🔥 9時〜10時の間に1回だけ
    if not (9 <= now.hour < 10):
        return

    db = SessionLocal()
    base_url = os.getenv("BASE_URL", "http://localhost:8000")

    stores = db.query(Store).all()

    for store in stores:

        # =========================
        # 1日1回制限（UTC対応）
        # =========================
        today = datetime.now(timezone.utc).date()
        start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)

        already_sent = db.query(Task).filter(
            Task.store_id == store.id,
            Task.title == "morning_sent",
            Task.created_at >= start
        ).first()

        if already_sent:
            continue

        links = db.query(StoreUser).filter(
            StoreUser.store_id == store.id
        ).all()

        if not links:
            continue

        # =========================
        # 店舗データ
        # =========================
        danger_reviews = db.query(Review).filter(
            Review.store_id == store.id,
            Review.reply_text.is_(None),
            Review.rating <= 2
        ).count()

        tasks = db.query(Task).filter(
            Task.store_id == store.id,
            Task.status == "open"
        ).count()

        last_post = db.query(Post).filter(
            Post.store_id == store.id
        ).order_by(Post.created_at.desc()).first()

        if last_post and last_post.created_at:
            stop_days = (datetime.now(timezone.utc) - last_post.created_at).days
        else:
            stop_days = 999

        # =========================
        # 店長ごとループ（ここが進化）
        # =========================
        for link in links:

            user = db.query(User).filter(
                User.id == link.user_id
            ).first()

            if not user or not user.line_user_id:
                continue

            # =========================
            # 個人行動ログ
            # =========================
            yesterday = datetime.utcnow() - timedelta(days=1)

            reply_done = db.query(ActionLog).filter(
                ActionLog.store_id == store.id,
                ActionLog.user_id == user.id,  # 🔥個人化
                ActionLog.action_type == "review_reply",
                ActionLog.created_at >= yesterday
            ).count()

            # =========================
            # 個人KPI
            # =========================
            review_kpi = 3

            # =========================
            # 個人リスク
            # =========================
            risk_score = danger_reviews * 3 + tasks + min(stop_days, 10) * 0.5

            if risk_score >= 10:
                danger_level = "🔴 危険"
            elif risk_score >= 5:
                danger_level = "🟡 注意"
            else:
                danger_level = "🟢 チャンス"

            # =========================
            # 個人プレッシャー
            # =========================
            if reply_done == 0:
                pressure = "🚨昨日0件 → このままだと評価下がる"
            elif reply_done < review_kpi:
                pressure = "⚠まだ足りてない"
            else:
                pressure = "✅いい流れ"

            # =========================
            # 褒め
            # =========================
            if reply_done >= review_kpi:
                praise = "👏しっかりやれてる"
            elif reply_done > 0:
                praise = "👍動けてる"
            else:
                praise = ""

            # =========================
            # トーン
            # =========================
            tones = [
                "ここだけやればOK",
                "3分で終わるから今やろ",
                "ここサボると売上落ちる",
                "ここやれば今日勝てる"
            ]
            tone = random.choice(tones)

            # =========================
            # メッセージ
            # =========================
            text = f"""【{store.name}｜{danger_level}】

{pressure}
{praise}

■最優先（{tone}）
・口コミ返信 {review_kpi}件

👇今すぐ
{base_url}/store/{store.id}/reviews

■昨日の実績
・返信：{reply_done}件

■ゴール
→ 今日の予約＋1件
"""

            send(user.line_user_id, text)

        # =========================
        # ログ
        # =========================
        log = Task(
            store_id=store.id,
            title="morning_sent",
            status="done"
        )
        db.add(log)
        db.commit()

    db.close()

    print("🔥 MORNING END")