def run():
    print("🔥 JOB 動いた")

    from app.services.line_notify import send_line
    send_line("朝タスク通知テスト")