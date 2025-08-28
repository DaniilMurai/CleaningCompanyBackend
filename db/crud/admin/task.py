from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_loader_criteria

import schemas
from db.crud.models.task import TaskCRUD
from db.models import Hint, Task


class AdminTaskCRUD(TaskCRUD):

    async def get_tasks(self):
        tasks = await self.db.execute(select(Task))
        return tasks.scalars().all()

    async def get_tasks_with_hints(
            self, params: schemas.AdminGetListParams | None = None
    ):
        stmt = select(self.model).where(
            self.model.is_deleted == False
        ).options(
            selectinload(self.model.hints),
            with_loader_criteria(Hint, Hint.is_deleted == False)
        )

        if params.order_by:
            field = params.order_by
            order = getattr(self.model, field)
            if params.direction == "asc":
                stmt = stmt.order_by(order.asc())
            else:
                stmt = stmt.order_by(order.desc())
        else:
            stmt = stmt.order_by(self.model.id.desc())

        stmt = await self.paginate(stmt, params.offset, params.limit)

        return (await self.db.execute(stmt)).scalars().all()
