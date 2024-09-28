from fastapi import APIRouter, Depends, HTTPException
from src.item.schemas import TaskItemCreate, TaskItemRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.database import get_async_session
from src.item.models import task_item
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/task_item', tags = ['TaskItem']
)

@router.post("/api/task/")
async def create_task_item(task: TaskItemCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(task_item).values(**task.model_dump())
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception as e:
        logger.error(f'Error {e}')
        raise HTTPException(status_code= 500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })

@router.get("/api/task/{id}", response_model=TaskItemRead)
async def read_task(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(task_item).where(task_item.c.id == id)
        result = await session.execute(query)
        task = result.fetchone()
        
        if task:
            task_dict = dict(task._asdict())
            return task_dict
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 
    
@router.put("/api/task/{id}")
async def update_task(id: int, task: TaskItemCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = update(task_item).where(task_item.c.id == id).values(**task.model_dump())
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 

@router.delete("/api/task/{id}", response_model=TaskItemRead)
async def delete_task(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = delete(task_item).where(task_item.c.id == id)
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 


