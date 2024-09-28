from fastapi import APIRouter, Depends, HTTPException
from src.record.schemas import TaskRecordCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.database import get_async_session
from src.record.models import task_record

router = APIRouter(
    prefix='/task_record', tags = ['TaskRecord']
)

@router.post("/api/task/")
async def create_task_item(task: TaskRecordCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(task_record).values(**task.dict())
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception:
        raise HTTPException(status_code= 500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })

@router.get("/api/task/{id}")
async def read_task(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(task_record).where(task_record.c.id == id)
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
async def update_task(id: int, task: TaskRecordCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = update(task_record).where(task_record.c.id == id).values(**task.model_dump())
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 

@router.delete("/api/task/{id}")
async def delete_task(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = delete(task_record).where(task_record.c.id == id)
        await session.execute(query)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 

