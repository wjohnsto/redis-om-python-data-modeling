import logging
import os
import aioredis

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from aredis_om.model import Migrator

from components.user.routes import router as user_router
from components.task.routes import router as task_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     await Migrator().run()
#     response = await call_next(request)
#     return response


@app.on_event("startup")
async def startup():
    await Migrator().run()
    logger = logging.getLogger("uvicorn.info")
    url = os.getenv('REDIS_OM_URL')
    if not url:
        url = 'redis://localhost:6379'
        logger.info("Using local redis")
    else:
        logger.info("Using redis from REDIS_OM_URL")

    r = aioredis.from_url(url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
