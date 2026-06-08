import requests

LINE_TOKEN = "3ff6GH2IkKi7aYuvCrmCQJEA2f3AfT7PODAs3hl/h989dDhhsHGJMdPRU9HuYxCGEVQgP45ktU05f1GYh1nUACzAeP6jvJFOuKdZ4EAkbrU6tWklDdb6YsyZc6r0aFPqy6QtOmfljbCeG0Y+BpMVlgdB04t89/1O/w1cDnyilFU="
USER_ID = "Uea9d5bf991230a9ff066272797da6cae"

def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": USER_ID,
        "messages": [
            {"type": "text", "text": message}
        ]
    }

    res = requests.post(url, headers=headers, json=data)

    print("STATUS:", res.status_code)
    print("BODY:", res.text)