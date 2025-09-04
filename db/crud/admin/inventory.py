from sqlalchemy import and_, select

import schemas
from db.crud.models.inventory import InventoryCRUD


class AdminInventoryCRUD(InventoryCRUD):

    # async def get_inventories(self):
    #     return (await self.db.execute(select(Inventory))).scalars().all()

    async def get_inventories_by_task_id(self, task_id: int) -> list[
        schemas.InventoryResponse]:
        result = (await self.db.execute(
            select(self.model).where(
                and_(self.model.task_id == task_id, self.model.is_deleted == False)
            )
        )).scalars().all()

        return [schemas.InventoryResponse.model_validate(r) for r in result]
