# service_base.py
from typing import Annotated, Generic, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel

import exceptions
import schemas
from api.admin.base.depends import AdminUserDepend
from db.crud.models.base import BaseModelCrud

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
ResponseSchema = TypeVar("ResponseSchema", bound=BaseModel)
AdminGetListParamsSchema = TypeVar("AdminGetListParamsSchema", bound=BaseModel)
CRUD = TypeVar("CRUD", bound=BaseModelCrud)


class AdminGenericService(
    Generic[CreateSchema, UpdateSchema, ResponseSchema, AdminGetListParamsSchema, CRUD]
):  # TODO Разобраться

    crud_cls: Type[CRUD]

    response_schema: Type[ResponseSchema]
    entity_name: str

    def __init__(
            self,
            admin: AdminUserDepend,
            crud: BaseModelCrud,  # Используем DI для CRUD
    ):
        self.admin = admin
        self.crud = crud

    def __init_subclass__(cls):
        def __init__(
                self,
                admin: AdminUserDepend,
                crud: Annotated[cls.crud_cls, Depends()],  # Используем DI для CRUD
        ):
            self.admin = admin
            self.crud = crud

        cls.__init__ = __init__

    async def get_list(
            self,
            params: AdminGetListParamsSchema | None = None
    ) -> list[ResponseSchema]:
        kwargs = params.model_dump(exclude_none=True) if params else {}
        items = await self.crud.get_list(**kwargs)
        return [self.response_schema.model_validate(item) for item in items]

    async def create(
            self,
            data: CreateSchema
    ) -> ResponseSchema:
        item = await self.crud.create(**data.model_dump(exclude_none=True))
        return self.response_schema.model_validate(item)

    async def create_list(
            self,
            data: list[CreateSchema]
    ) -> list[ResponseSchema]:
        pass

    async def update(
            self,
            item_id: int,
            data: UpdateSchema
    ) -> ResponseSchema:
        item = await self.crud.get(item_id)
        if not item:
            raise exceptions.ObjectNotFoundByIdError(self.entity_name, item_id)
        updated_item = await self.crud.update(item, data.model_dump(exclude_none=True))
        return self.response_schema.model_validate(updated_item)

    async def delete(
            self,
            item_id: int
    ) -> schemas.SuccessResponse:
        item = await self.crud.get(item_id)
        if not item:
            raise exceptions.ObjectNotFoundByIdError(self.entity_name, item_id)
        await self.crud.delete(item_id)
        return schemas.SuccessResponse(success=True)
