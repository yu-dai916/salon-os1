import osimport os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def generate_google_post_from_blog(
    title: str,
    excerpt: str,
    source_url: str,
    strategy_key: str,
    phone_number: str | None,
    cta_url: str | None,
    store_name: str,
) -> str:
    """
    戦略キーに沿って「予約に寄せる」投稿文を生成（短め）
    """
    phone = phone_number or ""
    cta = cta_url or ""
    strat = strategy_key or "reservation_push"

    sys = "You are a Japanese marketing copywriter for local beauty salons. Output only the final post text."
    user = f"""
店舗名: {store_name}
戦略キー: {strat}

元記事タイトル: {title}
元記事抜粋: {excerpt}
元記事URL: {source_url}

要件:
- Googleビジネスプロフィール投稿向け（短く強く）
- 予約/電話のCTAを必ず入れる（CTA URLがあればURL、なければ電話優先）
- 誇張しない。具体的で安心感あるトーン
- 最後に「詳しくはこちら: {source_url}」を入れる
- 電話: {phone}
- 予約URL: {cta}
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