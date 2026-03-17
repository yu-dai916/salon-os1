from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.task import Task

router = APIRouter(prefix="/tasks")


@router.get("/{store_id}")
def get_tasks(store_id: int, db: Session = Depends(get_db)):

    tasks = (
        db.query(Task)
        .filter(Task.store_id == store_id)
        .filter(Task.status == "open")
        .all()
    )

    return tasks