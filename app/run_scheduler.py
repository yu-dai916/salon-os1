import os
import time
from datetime import datetime

from app.queue import queue

RUN_ON_STARTUP = os.getenv("RUN_ON_STARTUP", "0") == "1"
INTERVAL_SECONDS = int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "300"))

last_morning_run = None


def is_morning():
    now = datetime.now()
    return now.hour == 9 and now.minute < 5


def main():
    global last_morning_run

    print("[scheduler] started")

    if not RUN_ON_STARTUP:
        print("[scheduler] idle")

        while True:
            time.sleep(60)

    while True:

        now = datetime.now()

        print("[scheduler] enqueue jobs")

        # 通常ジョブ
        queue.enqueue("app.jobs.fetch_hpb.run")
        #queue.enqueue("app.jobs.google_rank_job.run")
        queue.enqueue("app.jobs.google_reviews_job.run")
        #queue.enqueue("app.jobs.resolve_place_ids_job.run")
        queue.enqueue("app.jobs.store_score.run")
        queue.enqueue("app.scheduler.jobs.morning_notify.run")

        # 朝通知
        if is_morning():
            today = now.date()

            if last_morning_run != today:
                print("[scheduler] morning notify run")
                queue.enqueue("app.scheduler.jobs.morning_notify.run")
                last_morning_run = today

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()