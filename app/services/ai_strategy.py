def analyze_competition(store_rank, competitor_rank, reviews, competitor_reviews, posts):

    advice = []

    if store_rank and competitor_rank and store_rank > competitor_rank:
        advice.append("競合よりGoogle順位が低い")

    if competitor_reviews and reviews < competitor_reviews:
        advice.append("口コミ数が競合より少ない")

    if posts < 10:
        advice.append("Google投稿数が少ない")

    if not advice:
        advice.append("現在の施策は良好。投稿継続")

    return advice