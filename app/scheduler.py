import os
import time
from app.queue import queue


RUN_ON_STARTUP = os.getenv("RUN_ON_STARTUP", "0") == "1"
INTERVAL_SECONDS = int(os.getenv("SCHEDULER_INTERVAL_SECONDS", "300"))


def main():

    print("[scheduler] started")

    if not RUN_ON_STARTUP:
        print("[scheduler] idle")

        while True:
            time.sleep(60)

    while True:

        print("[scheduler] enqueue jobs")

        # HPBブログ取得
        queue.enqueue("app.jobs.fetch_hpb.run")

        # Google順位取得
        queue.enqueue("app.jobs.google_rank_job.run")

        # Google口コミ取得
        queue.enqueue("app.jobs.google_reviews_job.run")

        # PlaceID取得
        queue.enqueue("app.jobs.resolve_place_ids_job.run")

        # 店舗スコア計算
        queue.enqueue("app.jobs.store_score.run")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

    queue.enqueue("app.jobs.review_alert_job.run")
queue.enqueue("app.jobs.review_unreplied_job.run")
queue.enqueue("app.jobs.generate_tasks_job.run")
queue.enqueue("app.jobs.task_engine_job.run_task_engine")
queue.enqueue("app.jobs.serp_analysis_job.run")
