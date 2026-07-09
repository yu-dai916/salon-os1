def run():
    import os

    from app.services.google_reviews import fetch_and_save_reviews
    from app.db.session import SessionLocal
    from app.models.review import Review
    from app.services.line_notify import send_line

    print("🔥 DATABASE_URL =", os.getenv("DATABASE_URL"))
    print("🔥 NEW VERSION 🔥")

    db = SessionLocal()

    try:
        # 🔥 新規取得
        new_count = fetch_and_save_reviews()

        # 🔥 合計件数
        total_count = db.query(Review).count()

        # 🔥 メッセージ
        msg = f"🆕 新規口コミ {new_count}件（合計 {total_count}件）"

    except Exception as e:
        msg = f"❌ エラー: {e}"

    print("🔥 送信メッセージ:", msg)

    send_line(msg)

    db.close()


if __name__ == "__main__":
    run()
