import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def generate_review_reply(
    store_name: str,
    rating: int | None,
    comment: str,
    reviewer_name: str | None = None,
) -> str:
    sys = "You are a polite Japanese customer support specialist for beauty salons. Output only the reply text."
    user = f"""
店舗名: {store_name}
評価: {rating}
投稿者名: {reviewer_name}
口コミ本文:
{comment}

要件:
- 丁寧、短め、具体（次回来店につながる）
- 事実不明なことを断定しない
- クレームの場合は謝罪→改善→再来店の提案
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": user},
        ],
        temperature=0.6,
    )
    return (res.choices[0].message.content or "").strip()