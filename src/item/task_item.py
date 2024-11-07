from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from src.item.schemas import TaskItemCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.auth.models import User
from src.database import get_async_session
from src.item.models import task_item
from src.record.models import task_record
from src.auth.base_config import fastapi_users

router = APIRouter(
    prefix='/task_item', tags = ['TaskItem']
)

@router.get("/api/user_tasks/")
@cache(expire=60)
async def read_user_tasks(user: User = Depends(fastapi_users.current_user()), session: AsyncSession = Depends(get_async_session)):
    try:
        record_query = select(task_record).where(task_record.c.user_id == user.id)
        record_result = await session.execute(record_query)
        task_records = record_result.fetchall()

        tasks = []
        for record in task_records:
            record_dict = dict(record._asdict()) 

            task_query = select(task_item).where(task_item.c.id == record_dict['task_id'])
            task_result = await session.execute(task_query)
            task = task_result.fetchone()

            if task:
                task_dict = dict(task._asdict())
                tasks.append({
                    "task_id": task_dict['id'],                
                    "title": task_dict['title'],              
                    "description": task_dict['description'],  
                    "priority": task_dict['priority'],        
                    "due_date": task_dict['due_date'],         
                    "completion_date": record_dict['completion_date'], 
                    "time_spent": record_dict['time_spent']   
                })

        return tasks
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/user_task/")
async def create_tasks_item(task: TaskItemCreate, user: User = Depends(fastapi_users.current_user()),  session: AsyncSession = Depends(get_async_session)):
    try:
        # Add the task to the TaskItem
        stmt = insert(task_item).values(**task.model_dump())
        result = await session.execute(stmt)
        new_task_id = result.inserted_primary_key[0]  # Get the ID of the new task

        # Add a record to the TaskRecord to bind to the user
        task_record_stmt = insert(task_record).values(
            user_id=user.id,
            task_id=new_task_id,
            completion_date=None,  # By default, the task has not yet been completed
            time_spent=0  # Initial execution time
        )

        await session.execute(task_record_stmt)
        await session.commit()
        
        return {'status': 'success'}
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None,
        })

@router.put("/api/user_task/{id}")
async def update_user_task(id: int, task_data: TaskItemCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        task_stmt = (update(task_item).where(task_item.c.id == id).values(**task_data.model_dump()))
        await session.execute(task_stmt)
        await session.commit()

        return {"status": "success"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@router.put("/api/user_taskrecord/{id}")
async def update_user_taskrecord(
    id: int, 
    task_data: TaskItemCreate, 
    completion_date: datetime,
    time_spent: int,
    user: User = Depends(fastapi_users.current_user()), 
    session: AsyncSession = Depends(get_async_session)
):
    try:
        # Check that the user has access to this task
        record_query = select(task_record).where(task_record.c.user_id == user.id, task_record.c.task_id == id)
        record_result = await session.execute(record_query)
        record = record_result.fetchone()

        if record:
            task_stmt = (update(task_item).where(task_item.c.id == id).values(**task_data.model_dump()))
            await session.execute(task_stmt)

            record_update_stmt = (update(task_record).where(task_record.c.user_id == user.id, task_record.c.task_id == id)
                                .values(completion_date=completion_date, time_spent=time_spent))
            await session.execute(record_update_stmt)

            await session.commit()

        return {"status": "success"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@router.delete("/api/user_task/{id}")
async def delete_user_task(id: int, user: User = Depends(fastapi_users.current_user()), session: AsyncSession = Depends(get_async_session)):
    try:
        record_query = select(task_record).where(task_record.c.user_id == user.id, task_record.c.task_id == id)
        record_result = await session.execute(record_query)
        record = record_result.fetchone()

        if record:
            # Remove from task_record first so as not to break the foreign keys
            record_stmt = delete(task_record).where(task_record.c.user_id == user.id, task_record.c.task_id == id)
            await session.execute(record_stmt)

            # Remove from task_item
            task_stmt = delete(task_item).where(task_item.c.id == id)
            await session.execute(task_stmt)
            
            await session.commit() 

            return {'status': 'success'}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


