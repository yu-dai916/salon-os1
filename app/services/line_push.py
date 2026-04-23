import requests
import os

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")

def send_line(user_id, text):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": user_id,
        "messages": [
            {"type": "text", "text": text}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    print(res.status_code, res.text)