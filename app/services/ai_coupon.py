import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def generate_coupon_update_text(
    store_name: str,
    coupon_title: str,
    coupon_desc: str,
    expires_on: str,
    cta_url: str | None,
) -> str:
    sys = "You are a Japanese marketing copywriter for beauty salons. Output only the suggested update text."
    user = f"""
店舗名: {store_name}
クーポン名: {coupon_title}
説明: {coupon_desc}
期限: {expires_on}
予約URL: {cta_url}

要件:
- “期限が近い”前提の短い告知文
- 予約URLがあれば必ず入れる
- 誇張しない
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": user},
        ],
        temperature=0.7,
    )
    return (res.choices[0].message.content or "").strip()