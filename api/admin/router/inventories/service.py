import os

import schemas
from api.admin.base.service import AdminGenericService
from config import settings
from db.crud.admin.inventory import AdminInventoryCRUD
from utils.image_files import convert_base64_to_server_link


class AdminInventoryService(
    AdminGenericService[
        schemas.InventoryCreate,
        schemas.InventoryUpdate,
        schemas.InventoryResponse,
        schemas.AdminGetListParams,
        AdminInventoryCRUD
    ]
):
    response_schema = schemas.InventoryResponse
    entity_name = "inventory"
    crud_cls = AdminInventoryCRUD

    async def get_inventories_by_task_id(self, task_id: int) -> list[
        schemas.InventoryResponse]:
        return await self.crud.get_inventories_by_task_id(task_id)

    async def create_inventory(
            self, data: schemas.InventoryCreate
    ) -> schemas.InventoryResponse:
        file_urls = await convert_base64_to_server_link(
            data.media_links, path='inventories'
        )

        inventory = schemas.InventoryCreate(
            title=data.title,
            description=data.description,
            media_links=file_urls,
            task_id=data.task_id,
        )

        return await self.create(inventory)

    async def update_inventory(
            self, inventory_id: int, data: schemas.InventoryUpdate
    ) -> schemas.InventoryResponse:
        if not data.media_links:
            return await self.update(inventory_id, data)

        old_inventory = await self.crud.get(inventory_id)
        old_files = set(old_inventory.media_links)

        new_files = set(
            await convert_base64_to_server_link(data.media_links, path='inventories')
        )

        for old_file in old_files - new_files:
            filename = old_file.split('/')[-1]
            file_path = os.path.join(settings.IMAGES_HINTS_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        inventory = schemas.InventoryUpdate(
            title=data.title,
            description=data.description,
            media_links=list(new_files),
            task_id=data.task_id
        )
        return await self.update(inventory_id, inventory)
