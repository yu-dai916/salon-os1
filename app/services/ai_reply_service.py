import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reply(review_text: str) -> str:

    prompt = f"""
あなたは美容室の丁寧なカスタマーサポートです。
次のGoogle口コミへの返信を作成してください。

条件
・誠実
・改善意識
・短め（120文字前後）

口コミ:
{review_text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return res.choices[0].message.content.strip()