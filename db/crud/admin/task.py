from sqlalchemy import select

from db.crud.models.task import TaskCRUD
from db.models import Task


class AdminTaskCRUD(TaskCRUD):

    async def get_tasks(self):
        tasks = await self.db.execute(select(Task))
        return tasks.scalars().all()
