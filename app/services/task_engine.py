from sqlalchemy import func

from app.models.task import Task
from app.models import Review, Post


def generate_tasks(db, store_id):
    tasks = []

    unreplied = (
        db.query(func.count(Review.id))
        .filter(Review.store_id == store_id)
        .filter(Review.reply_text.is_(None))
        .scalar()
    ) or 0

    if unreplied > 0:
        tasks.append({
            "type": "review_reply",
            "title": "口コミ返信をする",
            "description": f"未返信口コミが {unreplied} 件あります"
        })

    posts = (
        db.query(func.count(Post.id))
        .filter(Post.store_id == store_id)
        .scalar()
    ) or 0

    if posts == 0:
        tasks.append({
            "type": "post_create",
            "title": "Google投稿を作成する",
            "description": "投稿がまだありません"
        })

    return tasks


def sync_tasks(db, store_id):
    new_tasks = generate_tasks(db, store_id)

    open_tasks = (
        db.query(Task)
        .filter(Task.store_id == store_id)
        .filter(Task.status == "open")
        .all()
    )

    open_task_map = {t.type: t for t in open_tasks}
    new_task_types = {t["type"] for t in new_tasks}

    # 新規タスク追加 or 既存更新
    for t in new_tasks:
        existing = open_task_map.get(t["type"])

        if existing:
            existing.title = t["title"]
            existing.description = t["description"]
        else:
            db.add(
                Task(
                    store_id=store_id,
                    type=t["type"],
                    title=t["title"],
                    description=t["description"],
                    status="open"
                )
            )

    # 今は不要になったopenタスクをdoneにする
    for old_task in open_tasks:
        if old_task.type not in new_task_types:
            old_task.status = "done"

    db.commit()