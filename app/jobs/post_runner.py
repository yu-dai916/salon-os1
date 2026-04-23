from app.db import get_db
from app.models import Post, Store
from app.queue import queue

def run():
    db = next(get_db())

    try:
        posts = db.query(Post).filter(
            Post.status.in_(["approved", "failed"])
        ).all()

        for post in posts:
            print("CHECK:", post.id, post.status)

            store = db.query(Store).filter(Store.id == post.store_id).first()

            if not store:
                print("NO STORE")
                continue

            if not store.google_place_id:
                print("NO PLACE ID")
                continue

            print("ENQUEUE:", post.id)

            try:
                queue.enqueue(
                    "app.jobs.post_to_google_rpa.run",
                    store.google_place_id,
                    post.content
                )

                post.status = "queued"

            except Exception as e:
                print("ENQUEUE ERROR:", e)
                post.status = "failed"
                post.last_error = str(e)

            db.commit()

    finally:
        db.close()