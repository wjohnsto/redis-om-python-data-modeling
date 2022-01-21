from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache.decorator import cache

from aredis_om.model import NotFoundError

from .model import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
async def save_user(user: User):
    return await user.save()


@router.get("")
async def list_users():
    return {"users": await User.find().all()}


@router.get("/{pk}")
@cache(expire=10)
async def get_user(pk: str):
    try:
        return await User.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
