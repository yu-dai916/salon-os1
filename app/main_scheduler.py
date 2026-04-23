import time
import os
from datetime import datetime, timedelta

from app.db import get_db
from app.jobs.fetch_hpb import run as fetch_hpb_run
from app.jobs.post_runner import run as post_runner
from app.jobs.morning_notify_job import run as morning_run


RUN_ON_STARTUP = os.getenv("RUN_ON_STARTUP", "1") == "1"
INTERVAL = int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "300"))

# 🔥 二重送信防止
last_morning_run = None

# 🔥 テストモード（Trueにすると毎回LINE飛ぶ）
TEST_MODE = True


def run():
    print("🚀 scheduler start")

    db = next(get_db())

    try:
        if RUN_ON_STARTUP:
            print("🔥 run on startup")

            try:
                fetch_hpb_run()
            except Exception as e:
                print("fetch_hpb error:", e)

            try:
                post_runner()
            except Exception as e:
                print("post_runner error:", e)

        while True:
            print("⏳ scheduler loop...")

            # JST変換
            now = datetime.utcnow() + timedelta(hours=9)

            global last_morning_run

            # =====================
            # 🔥 朝通知（テスト or 本番）
            # =====================
            if TEST_MODE:
                print("🔥 MORNING JOB RUN (TEST)")
                try:
                    morning_run()
                except Exception as e:
                    print("morning error:", e)

            else:
                # 本番用（8〜12時の間に1回）
                if 8 <= now.hour <= 12:
                    if not last_morning_run or last_morning_run.date() != now.date():
                        print("🔥 MORNING JOB RUN")
                        try:
                            morning_run()
                            last_morning_run = now
                        except Exception as e:
                            print("morning error:", e)

            # =====================
            # 通常ジョブ
            # =====================
            try:
                fetch_hpb_run()
            except Exception as e:
                print("fetch_hpb error:", e)

            try:
                post_runner()
            except Exception as e:
                print("post_runner error:", e)

            time.sleep(INTERVAL)

    finally:
        db.close()


if __name__ == "__main__":
    run()