from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from db.crud.models.base import BaseModelCrud
from db.models import DailyExtraTask, Task


class DailyExtraTaskCRUD(BaseModelCrud[DailyExtraTask]):
    model = DailyExtraTask

    # search_fields = ("daily_assignment_id", "room_id", "task_id")

    async def get_list_extra_tasks(self, daily_assignment_id: int):
        stmt = (
            select(DailyExtraTask)
            .where(
                and_(
                    DailyExtraTask.daily_assignment_id == daily_assignment_id,
                    DailyExtraTask.is_deleted == False
                )
            )
            .options(
                selectinload(DailyExtraTask.room),
                selectinload(DailyExtraTask.task),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_list_extra_tasks_with_hints(self, daily_assignment_id: int):
        stmt = (
            select(DailyExtraTask)
            .where(
                and_(
                    DailyExtraTask.daily_assignment_id == daily_assignment_id,
                    DailyExtraTask.is_deleted == False
                )
            )
            .options(
                selectinload(DailyExtraTask.room),
                selectinload(DailyExtraTask.task).selectinload(Task.hints),

            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
