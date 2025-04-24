from typing import Optional, Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select, ClauseElement, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.User.model import User


class AdminCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_unique_fields(self, exclude_user_id: int = None, **kwargs):
        query = select(User)

        for field, value in kwargs.items():
            query = query.where(getattr(User, field) == value)
        
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)

        result = await self.db.execute(query)
        if result.scalars().first():
            fields_str = ', '.join(f"{key}='{value}'" for key, value in kwargs.items())
            raise HTTPException(status_code=409, detail=f"User with {fields_str} already exists")

    async def get_user(
            self,
            *where_clauses: ClauseElement,
            skip: Optional[int] = None,
            limit: Optional[int] = None,
            single: bool = False,
            raise_not_found: bool = False,
            **filter_kwargs: Any,
    ) -> Row[Any] | RowMapping | Sequence[Row[Any] | RowMapping | Any]:
        """
        Универсальный метод получения User(ов).
        - where_clauses: SQLAlchemy-условия, например User.email == email
        - filter_kwargs: именованные фильтры — эквивалент filter_by(**)
        - skip/limit: пагинация
        - single: вернуть только первый результат (scalars().first())
        - raise_not_found: если single=True и нет результата — бросить 404
        """
        query = select(User)

        # добавляем WHERE
        for clause in where_clauses:
            query = query.where(clause)

        # добавляем filter_by
        if filter_kwargs:
            query = query.filter_by(**filter_kwargs)

        # пагинация
        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        result = await self.db.execute(query)
        scalars = result.scalars()

        if single:
            obj = scalars.first()
            if raise_not_found and obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return obj
        return scalars.all()
