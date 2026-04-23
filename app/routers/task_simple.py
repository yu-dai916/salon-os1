# app/api/routes/task_simple.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.task import Task

router = APIRouter(prefix="/simple-tasks", tags=["simple-tasks"])


@router.get("/store/{store_id}")
def store_tasks(store_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(
        Task.store_id == store_id,
        Task.type == "review_reply",
        Task.status == "open"
    ).all()


@router.get("/hq")
def hq_tasks(db: Session = Depends(get_db)):
    return db.query(Task).filter(
        Task.priority == "danger",
        Task.status == "open"
    ).all()