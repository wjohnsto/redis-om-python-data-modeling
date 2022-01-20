from ast import List
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from redis_om.model import NotFoundError
from redis_om.connections import get_redis_connection

from .model import Task, TaskAssignee

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("")
async def save_task(task: Task):
    return task.save()


@router.get("")
async def list_tasks(request: Request, response: Response):
    return {"tasks": Task.find().all()}

@router.get("/{pk}")
@cache(expire=10)
async def get_task(pk: str, request: Request, response: Response):
    print(pk)
    try:
        return Task.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="task not found")
