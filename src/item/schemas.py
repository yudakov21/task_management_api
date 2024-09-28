from pydantic import BaseModel
from abc import ABC, abstractmethod
from datetime import datetime
from src.item.models import PriorityLevel

class TaskItemCreate(BaseModel):
    id: int
    title: str
    description: str
    priority: PriorityLevel
    due_date: datetime

class TaskItemRead(BaseModel):
    id: int
    title: str
    description: str
    priority: PriorityLevel
    due_date: datetime



