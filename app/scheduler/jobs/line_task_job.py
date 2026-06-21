def run():
    from app.db import SessionLocal
    from app.models.review import Review
    from app.services.line_notify import send_line

    db = SessionLocal()

    # 未返信口コミ
    unreplied = db.query(Review).filter(Review.reply_text.is_(None)).count()

    msg = f"未返信口コミが {unreplied} 件あります"

    send_line(msg)

    db.close()


if __name__ == "__main__":
    run()