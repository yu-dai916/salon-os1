def run():
    import os

    from app.services.google_reviews import fetch_and_save_reviews
    from app.db.session import SessionLocal
    from app.models.review import Review
    from app.services.line_notify import send_line

    print("🔥 DATABASE_URL =", os.getenv("DATABASE_URL"))
    print("🔥 ALL STORES MODE 🔥")

    db = SessionLocal()

    try:
        # 🔥 全店舗の口コミ取得
        results = fetch_and_save_reviews()

        # 🔥 合計件数
        total_count = db.query(Review).count()

        # 🔥 メッセージ作成
        msg = "📊 本日の口コミ状況\n\n"

        for r in results:
            msg += f"【{r['store']}】\n🆕 新規口コミ {r['new_count']}件\n\n"

        msg += f"📈 合計口コミ数：{total_count}件"

    except Exception as e:
        msg = f"❌ エラー: {e}"

    print("🔥 送信メッセージ:", msg)

    send_line(msg)

    db.close()


if __name__ == "__main__":
    run()
