from statistics import mean

def diagnose(store, serp_rows, store_reviews, store_posts_last7):

    # 競合平均
    comp_reviews = [r.review_count for r in serp_rows if r.review_count]
    comp_rating  = [r.rating for r in serp_rows if r.rating]

    avg_reviews = int(mean(comp_reviews)) if comp_reviews else 0
    avg_rating  = round(mean(comp_rating), 2) if comp_rating else 0

    advice = []

    # 口コミ数
    if store_reviews < avg_reviews:
        advice.append(f"口コミ数が競合平均({avg_reviews})より少ない → 口コミ依頼を強化")

    # 投稿頻度（週）
    if store_posts_last7 < 2:
        advice.append("Google投稿が少ない → 週2回以上投稿")

    # 評価（目安）
    if avg_rating and avg_rating >= 4.6:
        advice.append("競合評価が高い → 低評価口コミの返信と接客改善を優先")

    if not advice:
        advice.append("競合と同等以上 → 写真投稿とスタイル更新で露出を維持")

    return {
        "avg_competitor_reviews": avg_reviews,
        "avg_competitor_rating": avg_rating,
        "store_reviews": store_reviews,
        "posts_last7_days": store_posts_last7,
        "advice": advice
    }