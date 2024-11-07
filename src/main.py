from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.auth.models import User
from src.auth.base_config import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.auth.manager import get_user_manager
from src.item.task_item import router as item_router
from src.record.task_record import router as record_router
from src.pages.router import router as page_router
from src.config import REDIS_HOST, REDIS_PORT
from redis import asyncio as aioredis


app = FastAPI(
    title='Tracker', debug=True, 
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(item_router)
app.include_router(record_router)
app.include_router(page_router)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encouding="utf8", decode_responses = True)
    FastAPICache.init(RedisBackend(redis), prefix = "fastapi-cache")