from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.task import Task

router = APIRouter(prefix="/test-store")


@router.get("/{store_id}", response_class=HTMLResponse)
def test_store(store_id: int, db: Session = Depends(get_db)):

    tasks = db.query(Task).filter(
        Task.store_id == store_id,
        Task.type == "review_reply",
        Task.status == "open"
    ).all()

    html = "<h1>口コミタスク</h1>"

    for t in tasks:
        html += f"<p>{t.description}</p>"

    return html