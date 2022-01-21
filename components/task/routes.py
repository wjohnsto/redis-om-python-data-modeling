from typing import Optional
from fastapi import APIRouter, HTTPException

from fastapi_cache.decorator import cache

from aredis_om.model import NotFoundError

from ..user.model import User

from .model import Task, TaskAssignee

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("")
async def save_task(task: Task):
    return await task.save()


@router.get("")
async def list_tasks(status: Optional[str] = None):
    if not status:
        return {
            "tasks": await Task.find().all()
        }

    return {
        "tasks": await Task.find(
            Task.status == "NEW"
        ).all()
    }


@router.get("/{pk}")
@cache(expire=10)
async def get_task(pk: str):
    try:
        return await Task.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")


@router.put("/{pk}")
async def update_task(pk: str, task: Task):
    try:
        db_task = await Task.get(pk)
        task.pk = db_task.pk

        if (len(task.assigned_to) <= 0):
            task.assigned_to = db_task.assigned_to

        return await db_task.update(
            name=task.name,
            status=task.status,
            description=task.description,
            assigned_to=task.assigned_to
        )
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")


@router.patch("/{pk}/assign/{user_pk}")
async def assign_task(pk: str, user_pk: str):
    try:
        task = await Task.get(pk)

        if not any(user.user_id == user_pk for user in task.assigned_to):
            task.assigned_to.append(
                TaskAssignee(user_id=user_pk)
            )
            await task.save()

        return task
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")


@router.get("/{pk}/assignees")
async def get_task_assignees(pk: str):
    try:
        task = await Task.get(pk)

        users = await User.find(
            User.pk << [user.user_id for user in task.assigned_to]
        ).all()

        return users
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")


@router.get("/user/{user_pk}")
@cache(expire=10)
async def get_user_tasks(user_pk: str, status: Optional[str] = None):
    try:
        if not status:
            return {
                "tasks": await Task.find(
                    Task.assigned_to.user_id == user_pk
                ).all()
            }

        return {
            "tasks": await Task.find(
                (Task.assigned_to.user_id == user_pk) &
                (Task.status == status)
            ).all()
        }
    except NotFoundError:
        raise HTTPException(status_code=404, detail="tasks not found")
