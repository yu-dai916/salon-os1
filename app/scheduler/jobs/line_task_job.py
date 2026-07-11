def run():
    import os

    from app.services.google_reviews import fetch_and_save_reviews
    from app.db.session import SessionLocal
    from app.models.review import Review
    from app.models.store import Store
    from app.models.store_user import StoreUser
    from app.services.line_notify import send_line

    print("🔥 START")
    print("🔥 DATABASE_URL =", os.getenv("DATABASE_URL"))

    db = SessionLocal()

    try:
        # 🔥 全店舗レビュー取得
        results = fetch_and_save_reviews()

        # 🔥 合計口コミ数
        total_count = db.query(Review).count()

        # 🔥 店舗ごとに分岐送信
        for r in results:
            store_name = r["store"]
            new_count = r["new_count"]

            # 🔥 変化ない店は送らない（重要）
            if new_count == 0:
                continue

            store = db.query(Store).filter(
                Store.name == store_name
            ).first()

            if not store:
                continue

            users = db.query(StoreUser).filter(
                StoreUser.store_id == store.id
            ).all()

            # 🔥 紐づいてるLINEユーザーにだけ送る
            for user in users:
                msg = f"📊 本日の口コミ状況\n\n【{store_name}】\n🆕 新規口コミ {new_count}件\n\n📈 合計口コミ数：{total_count}件"
                
                print(f"🔥 SEND → {store_name} → {user.line_user_id}")

                send_line(msg, user.line_user_id)

    except Exception as e:
        print("❌ エラー:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run()
