from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Enum as SQLAEnum, MetaData
import enum 

metadata = MetaData()

class PriorityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

task_item = Table(
    'task_item',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('title', String, index=True),
    Column('description', Text, nullable=True),
    Column('priority', SQLAEnum(PriorityLevel), default=PriorityLevel.medium),
    Column('due_date', DateTime),
)

