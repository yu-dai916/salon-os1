def analyze_store(rank, clicks, calls, posts, unreplied):

    advice = []

    if rank is None or rank > 5:
        advice.append("Google順位が弱い。口コミと投稿を増やす")

    if clicks is None or clicks < 20:
        advice.append("HPBクリックが少ない。スタイル写真とタイトル改善")

    if posts < 10:
        advice.append("Google投稿不足。週2投稿推奨")

    if unreplied > 0:
        advice.append("未返信口コミあり。24時間以内返信")

    if calls is not None and calls < 5:
        advice.append("電話導線弱い。投稿に予約CTA追加")

    if len(advice) == 0:
        advice.append("集客状態は良好。このまま継続")

    return advice