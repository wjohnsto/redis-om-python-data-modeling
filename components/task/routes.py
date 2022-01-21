from typing import Optional
from fastapi import APIRouter, HTTPException

from fastapi_cache.decorator import cache

from redis_om.model import NotFoundError

from .model import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("")
async def save_task(task: Task):
    return task.save()


@router.get("")
async def list_tasks(status: Optional[str] = None):
    if not status:
        return {
            "tasks": Task.find().all()
        }

    return {
        "tasks": Task.find(
            Task.status == "NEW"
        ).all()
    }


@router.get("/{pk}")
@cache(expire=10)
async def get_task(pk: str):
    print(pk)
    try:
        return Task.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")


@router.get("/user/{user_pk}")
@cache(expire=10)
async def get_user_tasks(user_pk: str, status: Optional[str] = None):
    try:
        if not status:
            return {
                "tasks": Task.find(
                    Task.assigned_to.user_id == user_pk
                ).all()
            }

        return {
            "tasks": Task.find(
                (Task.assigned_to.user_id == user_pk) &
                (Task.status == status)
            ).all()
        }
    except NotFoundError:
        raise HTTPException(status_code=404, detail="tasks not found")
