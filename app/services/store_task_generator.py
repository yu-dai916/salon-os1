def generate_tasks(rank, clicks, calls, posts, unreplied):
    tasks = []

    # 口コミ返信
    if unreplied > 0:
        tasks.append(f"未返信口コミ {unreplied}件 に返信（24時間以内）")

    # Google順位
    if rank is None or rank > 10:
        tasks.append("Google投稿を2件作成（検索キーワード入り）")

    # HPBクリック
    if clicks is None or clicks < 20:
        tasks.append("スタイル写真を3枚追加（顔周り・レイヤー・ビフォーアフター）")

    # 投稿数
    if posts < 2:
        tasks.append("今週Google投稿を2回実施（予約導線リンク付き）")

    # 電話
    if calls is not None and calls < 5:
        tasks.append("投稿文に『電話予約はこちら』CTAを追加")

    if len(tasks) == 0:
        tasks.append("今週は大きな改善タスクなし。現状の投稿と口コミ返信を継続")

    return tasks