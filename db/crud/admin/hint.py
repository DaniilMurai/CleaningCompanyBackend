from sqlalchemy import and_, select

import schemas
from db.crud.models.hint import HintCRUD
from db.models import Hint


class AdminHintsCRUD(HintCRUD):

    async def get_hints(self):
        return (await self.db.execute(select(Hint))).scalars().all()

    async def get_hints_by_task_id(self, task_id: int) -> list[schemas.HintsResponse]:
        result = (await self.db.execute(
            select(self.model).where(
                and_(self.model.task_id == task_id, self.model.is_deleted == False)
            )
        )).scalars().all()

        return [schemas.HintsResponse.model_validate(r) for r in result]
