import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def generate_reply(review_text: str) -> str:
    if not client:
        return "（デモ）ご来店ありがとうございます。またお待ちしております。"

    prompt = f"""
美容室の口コミ返信を書いてください

口コミ:
{review_text}

条件
・丁寧
・来店感謝
・次回来店導線
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception:
        return "（デモ）ご来店ありがとうございます。またお待ちしております。"


def generate_reply_with_strategy(comment: str):
    if not client:
        return "デモ返信", "（デモ）ご来店ありがとうございます。またお待ちしております。"

    prompt = f"""
あなたは美容室の口コミ対応のプロです。

まず、この口コミに対して最適な対応戦略を1つ選んでください。

戦略の種類：
・謝罪
・改善説明
・感謝強化
・再来店促進

その後、その戦略に基づいて返信を書いてください。

口コミ:
{comment}

出力形式：
戦略: ○○
返信:
○○○
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        text = res.choices[0].message.content or ""

        strategy = ""
        reply = ""

        if "返信:" in text:
            parts = text.split("返信:")
            strategy = parts[0].replace("戦略:", "").strip()
            reply = parts[1].strip()
        else:
            strategy = "通常返信"
            reply = text.strip()

        if not reply:
            reply = "ご来店ありがとうございます。またお待ちしております。"

        return strategy, reply

    except Exception:
        return "デモ返信", "（デモ）ご来店ありがとうございます。またお待ちしております。"