def calc_store_score(rank, clicks, calls, posts, unreplied_reviews):

    score = 100

    # Google順位
    if rank is None:
        score -= 30
    elif rank > 10:
        score -= 20
    elif rank > 5:
        score -= 10

    # HPBクリック
    if clicks is not None and clicks < 10:
        score -= 15

    # 電話
    if calls is not None and calls < 5:
        score -= 15

    # 投稿
    if posts < 5:
        score -= 10

    # 口コミ未返信
    if unreplied_reviews > 10:
        score -= 20
    elif unreplied_reviews > 5:
        score -= 10

    return max(score, 0)