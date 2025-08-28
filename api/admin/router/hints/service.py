import os

import schemas
from api.admin.base.service import AdminGenericService
from config import settings
from db.crud.admin.hint import AdminHintsCRUD
from utils.image_files import convert_base64_to_server_link


class AdminHintService(
    AdminGenericService[
        schemas.HintsCreate,
        schemas.HintsUpdate,
        schemas.HintsResponse,
        schemas.AdminGetListParams,
        AdminHintsCRUD
    ]
):
    response_schema = schemas.HintsResponse
    entity_name = "hint"
    crud_cls = AdminHintsCRUD

    async def get_hints_by_task_id(self, task_id: int) -> list[schemas.HintsResponse]:
        return await self.crud.get_hints_by_task_id(task_id)

    async def create_hint(self, data: schemas.HintsCreate) -> schemas.HintsResponse:
        file_urls = await convert_base64_to_server_link(data.media_links, path='hints')

        hint = schemas.HintsCreate(
            title=data.title,
            text=data.text,
            media_links=file_urls,
            task_id=data.task_id,
        )

        return await self.create(hint)

    async def update_hint(
            self, hint_id: int, data: schemas.HintsUpdate
    ) -> schemas.HintsResponse:
        if not data.media_links:
            return await self.update(hint_id, data)

        old_hint = await self.crud.get(hint_id)
        old_files = set(old_hint.media_links)

        new_files = set(
            await convert_base64_to_server_link(data.media_links, path='hints')
        )

        for old_file in old_files - new_files:
            filename = old_file.split('/')[-1]
            file_path = os.path.join(settings.IMAGES_HINTS_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        hint = schemas.HintsUpdate(
            title=data.title,
            text=data.text,
            media_links=list(new_files),
            task_id=data.task_id
        )
        return await self.update(hint_id, hint)

    # @staticmethod
    # async def convert_base64_to_server_link(base64_links: list[str]) -> list[str]:
    #     file_urls = []
    #     for base64_link in base64_links:
    #
    #         if base64_link.startswith("http"):
    #             file_urls.append(base64_link)
    #             continue
    #
    #         if "," not in base64_link:
    #             continue
    #
    #         header, encoded = base64_link.split(",", 1)
    #         ext = header.split("/")[1].split(";")[0]
    #         unique_name = f"{uuid.uuid4()}.{ext}"
    #
    #         file_path = os.path.join(
    #             settings.IMAGES_HINTS_DIR, unique_name
    #         )
    #
    #         async with aiofiles.open(file_path, "wb") as f:
    #             await f.write(base64.b64decode(encoded))
    #
    #         file_urls.append(f"{settings.BASE_URL}/images/hints/{unique_name}")
    #     print(file_urls)
    #     return file_urls
