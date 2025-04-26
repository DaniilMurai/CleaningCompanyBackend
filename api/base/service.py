from typing import Annotated, Generic, TypeVar

from fastapi import Depends

T = TypeVar("T")


class BaseCrudService(Generic[T]):
    def __init__(self, crud: Annotated[T, Depends()]):
        self.crud = crud
