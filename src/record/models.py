from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, MetaData
from src.item.models import task_item
from src.auth.models import user

metadata = MetaData()

task_record = Table(
    'task_record',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('user_id', Integer, ForeignKey(user.c.id)),
    Column('task_id', Integer, ForeignKey(task_item.c.id)),
    Column('completion_date', DateTime),
    Column('time_spent', Integer),
)