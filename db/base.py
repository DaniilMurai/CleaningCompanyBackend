from sqlalchemy import Boolean, Column, Integer, false
from sqlalchemy.orm import DeclarativeBase, declared_attr

from utils.text import paschal_case_to_snake_case


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_deleted = Column(
        Boolean, server_default=false(), default=False, nullable=False
    )

    @declared_attr
    def __tablename__(self):
        """
        Defines __tablename__ for child class,
        so it doesn't have to be defined manually in every model,
        it can be redefined in subclass though
        """
        return paschal_case_to_snake_case(self.__name__) + "s"

    pass
