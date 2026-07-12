def run():
    import os

    from app.services.google_reviews import fetch_and_save_reviews
    from app.db.session import SessionLocal
    from app.models.review import Review
    from app.models.store import Store
    from app.models.store_user import StoreUser
    from app.models.user import User
    from app.services.line_notify import send_line

    print("🔥 START")
    print("🔥 DATABASE_URL =", os.getenv("DATABASE_URL"))

    db = SessionLocal()

    try:
        # 🔥 全店舗レビュー取得
        results = fetch_and_save_reviews()

        # 🔥 合計口コミ数
        total_count = db.query(Review).count()

        # 🔥 店舗ごとに通知
        for r in results:
            store_name = r["store"]
            new_count = r["new_count"]

            # 🔥 変化ない店は送らない（重要）
            if new_count == 0:
                continue

            # 🔥 店舗取得
            store = db.query(Store).filter(
                Store.name == store_name
            ).first()

            if not store:
                print(f"❌ 店舗見つからん: {store_name}")
                continue

            # 🔥 店舗に紐づくユーザー取得
            store_users = db.query(StoreUser).filter(
                StoreUser.store_id == store.id
            ).all()

            print(f"🏪 {store_name} → users: {store_users}")

            for su in store_users:
                # 🔥 UserテーブルからLINE ID取得
                user = db.query(User).filter(
                    User.id == su.user_id
                ).first()

                if not user:
                    print("❌ Userなし")
                    continue

                if not user.line_user_id:
                    print("❌ LINE IDなし")
                    continue

                # 🔥 送信メッセージ
                msg = f"""📊 本日の口コミ状況

【{store_name}】
🆕 新規口コミ {new_count}件

📈 合計口コミ数：{total_count}件
"""

                print(f"🔥 SEND → {store_name} → {user.line_user_id}")

                send_line(msg, user.line_user_id)

    except Exception as e:
        print("❌ エラー:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run()
