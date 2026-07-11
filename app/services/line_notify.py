import requests
import os

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")


def send_line(message, user_id):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": user_id,  # 🔥 ここが核心
        "messages": [
            {"type": "text", "text": message}
        ]
    }

    res = requests.post(url, headers=headers, json=data)

    print("STATUS:", res.status_code)
    print("BODY:", res.text)
