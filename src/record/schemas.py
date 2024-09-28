from pydantic import BaseModel
from abc import ABC, abstractmethod
from datetime import datetime

class TaskRecordCreate(BaseModel):
    user_id: int
    task_id: int
    completion_date: datetime
    time_spent: int

class TaskRecordRead(BaseModel):
    id: int
    user_id: int
    task_id: int
    completion_date: datetime
    time_spent: int
