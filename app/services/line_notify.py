import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")


def send_line(message: str):
    url = "https://notify-api.line.me/api/notify"

    try:
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {LINE_TOKEN}"
            },
            data={"message": message},
            timeout=5
        )

        print("LINE STATUS:", res.status_code)
        print("LINE RESPONSE:", res.text)

    except Exception as e:
        print("LINE ERROR:", str(e))