from fastapi import FastAPI
from fastapi_users import fastapi_users, FastAPIUsers
from src.auth.models import User
from src.auth.base_config import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.auth.manager import get_user_manager
from src.item.task_item import router as item_router
from src.record.task_record import router as record_router

app = FastAPI(
    title='Tracker'
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