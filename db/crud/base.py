from typing import Annotated, Type, TypeVar

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..depends import DBDepend

T = TypeVar("T")


class CRUD:
    _depends = None

    def __init__(
            # Annotated[] adds Depends() automatically,
            # so it can be used as Depend,
            # it doesn't change the class __init__ method though
            # so it can be used as usual class CRUD(db)
            self, db: Annotated[AsyncSession, DBDepend]
    ):
        self.db = db

    @classmethod
    def depends(cls: Type[T]) -> Type[T]:
        if not cls._depends:
            cls._depends = Annotated[cls, Depends()]
        return cls._depends
