from typing import Any, Generic, List, Type, TypeVar

from sqlalchemy import asc, desc, or_, select

import exceptions
from db.base import Base
from db.crud.base import CRUD

T = TypeVar("T", bound=Base)


class BaseModelCrud(CRUD, Generic[T]):
    model: Type[Base]
    search_fields: tuple[str, ...] | None = None

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

    async def get_list(
            self, *,
            search: str | None = None,
            order_by: Any | tuple[Any, ...] | None = None,
            offset: int | None = None,
            limit: int | None = None,
            direction: str | None = None,
            **kwargs,
    ) -> List[T]:
        stmt = self.get_statement(**kwargs)
        if search:
            if not self.search_fields:
                raise ValueError("search_fields is required for search to work")

            stmt = stmt.where(
                or_(
                    *[
                        getattr(self.model, field).contains(search)
                        for field in self.search_fields
                    ]
                )
            )

        if order_by:
            field = order_by
            column = getattr(self.model, field)

            if direction == "desc":
                stmt = stmt.order_by(desc(column))
            else:
                stmt = stmt.order_by(asc(column))
        else:
            stmt = stmt.order_by(desc(self.model.id))

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.db.scalars(stmt)
        return result.all()

    async def pre_process_update_data(
            self, data: dict,
            current_obj_id: int | None = None
    ) -> dict:
        return data

    async def update(self, obj: T, __data: dict | None = None, **kwargs) -> T:
        data = await self.pre_process_update_data(
            {
                **(__data or {}),
                **kwargs
            },
            obj.id
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
        await self.db.commit()
        return obj

    async def delete(self, id: int):
        obj = await self.get(id)
        if not obj:
            raise exceptions.ObjectNotFoundByIdError(self.model.__name__, id)
        await self.db.delete(obj)
        await self.db.commit()
