from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.crud.models.base import BaseModelCrud
from db.models import DailyExtraTask


class DailyExtraTaskCRUD(BaseModelCrud[DailyExtraTask]):
    model = DailyExtraTask

    # search_fields = ("daily_assignment_id", "room_id", "task_id")

    async def get_list_extra_tasks(self, daily_assignment_id: int):
        stmt = (
            select(DailyExtraTask)
            .where(DailyExtraTask.daily_assignment_id == daily_assignment_id)
            .options(
                selectinload(DailyExtraTask.task),
                selectinload(DailyExtraTask.room)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
