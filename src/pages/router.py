from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.item.task_item import read_user_tasks
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.database import get_async_session
from fastapi.responses import HTMLResponse
from src.item.models import task_item
from src.record.models import task_record

router = APIRouter(
    prefix='/pages',
    tags=["Pages"]
)

templates = Jinja2Templates(directory='src/templates')

@router.get("/base")
def get_base_pages(request: Request, user: User = Depends(fastapi_users.current_user(optional=True))):
    return templates.TemplateResponse("base.html", {"request":request, "user": user, })

@router.get("/login", response_class=HTMLResponse)
def gen_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
def gen_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#!
@router.get("/task_list")
async def get_task_list(request: Request, user: User = Depends(fastapi_users.current_user()), session: AsyncSession = Depends(get_async_session)):
    tasks = await read_user_tasks(user=user, session=session)
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks, "user": user})

@router.get("/task_list/add_task")
async def get_add_task(request: Request, user: User = Depends(fastapi_users.current_user())):
    return templates.TemplateResponse("add_task.html", {"request": request, "user": user})

@router.get("/task_list/edit/{id}", response_class=HTMLResponse)
async def get_task_for_edit(
    id: int, 
    request: Request, 
    user: User = Depends(fastapi_users.current_user()), 
    session: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем запись задачи для текущего пользователя
        record_query = select(task_record).where(task_record.c.user_id == user.id, task_record.c.task_id == id)
        record_result = await session.execute(record_query)
        record = record_result.fetchone()

        if not record:
            raise HTTPException(status_code=404, detail="Task not found or access denied")

        # Получаем саму задачу
        task_query = select(task_item).where(task_item.c.id == id)
        task_result = await session.execute(task_query)
        task = task_result.fetchone()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return templates.TemplateResponse("edit_task.html", {
            "request": request, 
            "task": dict(task._asdict()), 
            "record": dict(record._asdict()),
            "user": user
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


