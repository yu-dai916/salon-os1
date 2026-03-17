from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_store(store, serp_rows):

    competitors = "\n".join([
        f"{r.name} 評価{r.rating} 口コミ{r.review_count}"
        for r in serp_rows
    ])

    prompt = f"""
あなたは美容室のGoogle集客コンサルタントです。

店舗
{store.name}

競合SERP
{competitors}

この店舗が順位を上げるために必要な改善を3つ出してください。
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content