def run():
    import os

    from app.services.google_reviews import fetch_and_save_reviews
    fetch_and_save_reviews()  # ←これ追加🔥

    # 🔥 env確認
    print("🔥 DATABASE_URL (env) =", os.getenv("DATABASE_URL"))
    print("🔥 NEW VERSION 🔥")

    import app.db.session
    print("🔥 実際に読まれてるパス:", app.db.session.__file__)

    from app.db.session import SessionLocal
    from app.models.review import Review
    from app.services.line_notify import send_line

    db = SessionLocal()

    try:
        count = db.query(Review).count()
        msg = f"DB接続OK：レビュー {count} 件"
    except Exception as e:
        msg = f"DBエラー: {e}"

    print("🔥 送信メッセージ:", msg)

    send_line(msg)

    db.close()


if __name__ == "__main__":
    run()
