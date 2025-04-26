from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select

import exceptions
from db.base import Base
from db.crud.base import CRUD

T = TypeVar("T", bound=Base)


class BaseModelCrud(CRUD, Generic[T]):
    model: Type[Base]

    @classmethod
    def get_statement(cls, **kwargs):
        return (
            select(cls.model)
            .filter_by(**kwargs)
        )

    async def get(self, id: Any = None, **kwargs) -> T | None:
        if isinstance(id, self.model):
            if not kwargs:
                return id
            kwargs["id"] = id.id

        if id:
            kwargs["id"] = id
        elif not kwargs:
            return None

        stmt = self.get_statement(**kwargs)
        return await self.db.scalar(stmt)

    async def pre_process_update_data(self, data: dict) -> dict:
        return data

    async def update(self, obj: T, __data: dict | None = None, **kwargs) -> T:
        data = await self.pre_process_update_data(
            {
                **(__data or {}),
                **kwargs
            }
        )
        if not data:
            return obj
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        return obj

    async def pre_process_create_data(self, data: dict) -> dict:
        return data

    async def create(self, __data: dict | None = None, **kwargs) -> T:
        data = await self.pre_process_create_data(
            {
                **(__data or {}),
                **kwargs
            }
        )
        obj = self.model(**data)
        self.db.add(obj)
        return obj

    async def delete(self, id: int):
        obj = await self.get(id)
        if not obj:
            raise exceptions.ObjectNotFoundByIdError(self.model.__name__, id)
        await self.db.delete(obj)
