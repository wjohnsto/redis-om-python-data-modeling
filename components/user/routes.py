from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from redis_om.model import NotFoundError
from redis_om.connections import get_redis_connection

from .model import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("")
async def save_user(user: User):
    # We can save the model to Redis by calling `save()`:
    return user.save()


@router.get("")
async def list_users(request: Request, response: Response):
    return {"users": User.find().all()}


@router.get("/{pk}")
@cache(expire=10)
async def get_user(pk: str, request: Request, response: Response):
    # To retrieve this user with its primary key, we use `user.get()`:
    try:
        return User.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
