from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..depends import get_db


class CRUD:
    def __init__(
            # Annotated[] adds Depends() automatically,
            # so it can be used as Depend,
            # it doesn't change the class __init__ method though
            # so it can be used as usual class CRUD(db)
            self, db: Annotated[AsyncSession, Depends(get_db)]
    ):
        self.db = db
