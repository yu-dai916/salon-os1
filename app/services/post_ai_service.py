import os
from openai import OpenAI

client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def generate_google_post_from_blog(
    title: str,
    excerpt: str,
    source_url: str,
    strategy_key: str,
    phone_number: str | None,
    cta_url: str | None,
    store_name: str,
    area: str,
    main_menu: str,
) -> str:

    phone = phone_number or ""
    cta = cta_url or ""
    strat = strategy_key or "reservation_push"

    prompt = f"""
あなたは美容室のローカルSEOマーケターです。

【店舗名】{store_name}
【地域】{area}
【メニュー】{main_menu}

【元タイトル】
{title}

【本文】
{excerpt}

【ルール】
・「{area} 美容室」を必ず入れる
・「{main_menu}」を必ず入れる
・100〜200文字
・具体的に書く（抽象NG）
・最後に予約CTA

予約: {cta}
電話: {phone}

出力：
タイトル：
本文：
"""

    res = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return res.choices[0].message.content