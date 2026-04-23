from app.services.line_push import send_line
from app.models.store_user import StoreUser
from app.models.user import User


def notify_store_users(db, store_id, text):
    print("🔥 notify開始", store_id)

    store_users = db.query(StoreUser).filter(StoreUser.store_id == store_id).all()

    print("🔥 users数", len(store_users))

    for su in store_users:
        print("🔥 user_id", su.user_id)

        user = db.query(User).filter(User.id == su.user_id).first()

        if user and user.line_user_id:
            print("🔥 LINE送信", user.line_user_id)
            send_line(user.line_user_id, text)