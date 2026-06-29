def run():
    import os

    print("🔥🔥🔥 DATABASE_URL 👉", os.getenv("DATABASE_URL"))

    from app.db import SessionLocal
    from app.models.review import Review
    from app.services.line_notify import send_line

    db = SessionLocal()

    try:
        count = db.query(Review).count()
        msg = f"DB接続OK：レビュー {count} 件"
    except Exception as e:
        msg = f"DBエラー: {e}"

    send_line(msg)

    db.close()


if __name__ == "__main__":
    run()
