from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.database import get_async_session
from src.record.models import task_record
from src.record.schemas import TaskRecordCreate
from src.item.schemas import TaskItemCreate, TaskItemRead
from src.item.models import task_item

router = APIRouter(
    prefix='/task_record', tags = ['TaskRecord']
)

@router.post("/api/record/")
async def create_task_item(record: TaskRecordCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(task_record).values(**record.dict())
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success'}
    except Exception:
        raise HTTPException(status_code= 500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })

@router.get("/api/record/{id}")
async def read_record(id: int, session: AsyncSession = Depends(get_async_session)):
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
    
@router.put("/api/record/{id}")
async def update_record(id: int, record: TaskRecordCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(task_record).where(task_record.c.id == id).values(**record.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 

@router.delete("/api/record/{id}")
async def delete_record(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(task_record).where(task_record.c.id == id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 

@router.post("/api/task/")
async def create_task_item(task: TaskItemCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(task_item).values(**task.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success'}
    except Exception as e:
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
        stmt = update(task_item).where(task_item.c.id == id).values(**task.model_dump())
        await session.execute(stmt)
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
        stmt = delete(task_item).where(task_item.c.id == id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'success'}
    except Exception:
            raise HTTPException(status_code= 500, detail={
                'status': 'error',
                'data': None,
                'details': None,
            }) 