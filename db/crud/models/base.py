from typing import Any, Generic, List, Type, TypeVar

from sqlalchemy import Select, asc, desc, exists, or_, select
from sqlalchemy.orm import DeclarativeBase

import exceptions
from api.base.exception_handlers import logger
from db.base import Base
from db.crud.base import CRUD

T = TypeVar("T", bound=Base)


class BaseModelCrud(CRUD, Generic[T]):
    model: Type[Base]
    search_fields: tuple[str, ...] | None = None

    @classmethod
    def get_statement(cls, model: Type[Base] | None = None, **kwargs):

        return (
            select(model or cls.model)
            .filter_by(**kwargs)
            .filter_by(is_deleted=False)
        )

    @staticmethod
    async def paginate(
            stmt: Select[tuple[Base]], offset: int | None = None,
            limit: int | None = None
    ):
        print("offset", offset)
        print("limit", limit)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        return stmt

    async def get(
            self, id: Any = None, model: Type[Base] | None = None, f: str = "id",
            **kwargs
    ) -> T | None:
        current_model = model or self.model

        stmt = self.get_statement(current_model, **kwargs)

        # если указан id, то использовать его с полем f
        if id is not None:
            field_column = getattr(current_model, f)
            stmt = stmt.where(field_column == id)

        # если нет id, но есть kwargs, то get_statement уже добавил фильтры
        if id is None and not kwargs:
            return None

        return await self.db.scalar(stmt)

    async def get_list(
            self, *,
            search: str | None = None,
            order_by: Any | tuple[Any, ...] | None = None,
            offset: int | None = None,
            limit: int | None = None,
            model: Type[Base] | None = None,
            direction: str | None = None,
            ids: list[int] | None = None,
            f: str = "id",
            **kwargs,
    ) -> List[T]:
        current_model = model or self.model

        stmt = self.get_statement(current_model, **kwargs)

        if ids is not None:
            column = getattr(current_model, f)
            stmt = stmt.where(column.in_(ids))

        if search:
            if not self.search_fields:
                raise ValueError("search_fields is required for search to work")

            stmt = stmt.where(
                or_(
                    *[
                        getattr(current_model, field).contains(search)
                        for field in self.search_fields
                    ]
                )
            )

        if order_by:
            field = order_by
            column = getattr(current_model, field)

            if direction == "desc":
                stmt = stmt.order_by(desc(column))
            else:
                stmt = stmt.order_by(asc(column))
        else:
            stmt = stmt.order_by(desc(current_model.id))

        stmt = await self.paginate(stmt, offset, limit)

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

    async def pre_process_create_data(self, data: dict | list[dict]) -> dict | list[
        dict]:
        return data

    async def create_batch(self, __data: list[dict]) -> list[Base] | list[Any] | None:

        if not __data:
            return []
        data_list = await self.pre_process_create_data(__data)
        objects = [self.model(**item) for item in data_list]

        try:
            self.db.add_all(objects)

            await self.db.flush()

            await self.db.execute(
                select(self.model).where(
                    self.model.id.in_([obj.id for obj in objects])
                )
            )

            await self.db.commit()
            return objects

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Batch create failed: {str(e)}")

    async def create(
            self, __data: dict | None = None, model: Type[Base] | None = None, **kwargs
    ) -> T:
        current_model = model or self.model
        data = await self.pre_process_create_data(
            {
                **(__data or {}),
                **kwargs
            }
        )
        obj = current_model(**data)
        self.db.add(obj)
        await self.db.commit()
        return obj

    async def delete(self, id: int):
        obj = await self.get(id)
        if not obj:
            raise exceptions.ObjectNotFoundByIdError(self.model.__name__, id)
        await self.update(obj, is_deleted=True)

    async def restore(self, id: int):
        obj = await self.get(id)
        if not obj:
            raise exceptions.ObjectNotFoundByIdError(self.model.__name__, id)
        await self.update(obj, is_deleted=False)

    async def get_deleted_list(self, **kwargs) -> List[T]:
        stmt = select(self.model).filter_by(**kwargs, is_deleted=True)
        return await self.db.scalars(stmt).all()

    async def exists(self, model: Type[DeclarativeBase], **filters) -> bool:
        result = await self.db.execute(
            select(
                exists().where(*[getattr(model, k) == v for k, v in filters.items()])
            )
        )
        return result.scalar()

    async def exists(
            self,
            model: Type[DeclarativeBase],
            include_deleted: bool = False,  # Новый параметр
            **filters
    ) -> bool:
        conditions = [getattr(model, k) == v for k, v in filters.items()]

        # Добавляем условие только если не запрошены удалённые
        if not include_deleted and hasattr(model, 'is_deleted'):
            conditions.append(model.is_deleted == False)

        result = await self.db.execute(select(exists().where(*conditions)))
        return result.scalar()
