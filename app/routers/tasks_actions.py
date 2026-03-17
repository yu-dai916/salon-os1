from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.task import Task

router = APIRouter()


@router.post("/tasks/{task_id}/done")
def done_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task:
        task.status = "done"
        db.commit()
        return RedirectResponse(url=f"/store/{task.store_id}/page", status_code=303)

    return {"ok": False}