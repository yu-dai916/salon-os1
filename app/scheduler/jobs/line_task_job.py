def run():
    from app.services.line_notify import send_line

    msg = "テスト：LINE通知成功"

    send_line(msg)


if __name__ == "__main__":
    run()