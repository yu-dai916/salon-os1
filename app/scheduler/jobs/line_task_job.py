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
        # 🔥 ① 最新レビュー取得（DB更新）
        fetch_and_save_reviews()

        # 🔥 ② 全店舗取得
        stores = db.query(Store).all()

        for store in stores:
            store_name = store.name

            # 🔥 ③ ★1・★2 & 未返信のみ取得
            bad_reviews = db.query(Review).filter(
                Review.store_id == store.id,
                Review.rating <= 2,
                Review.reply_text.is_(None)
            ).all()

            if not bad_reviews:
                continue  # 🔥 無ければスキップ

            print(f"🚨 {store_name} 危険レビューあり: {len(bad_reviews)}件")

            # 🔥 ④ 店舗に紐づくユーザー取得
            store_users = db.query(StoreUser).filter(
                StoreUser.store_id == store.id
            ).all()

            for su in store_users:
                user = db.query(User).filter(
                    User.id == su.user_id
                ).first()

                if not user or not user.line_user_id:
                    continue

                # 🔥 ⑤ レビューごとに送信
                for br in bad_reviews:
                    msg = f"""🚨【{store_name}】

★{br.rating}の口コミあり

「{(br.comment or '')[:50]}」

👉 すぐ返信してください
"""

                    print(f"🔥 SEND → {store_name} → {user.line_user_id}")

                    send_line(msg, user.line_user_id)

    except Exception as e:
        print("❌ エラー:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run()
