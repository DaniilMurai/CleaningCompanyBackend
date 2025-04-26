import enum
import json
import logging
import traceback
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from types import FunctionType
from typing import Any, Iterable, Protocol, TypeAlias

from .base import BaseSyncLogger


class ObjWithToPythonMethodProtocol(Protocol):
    def to_python(self) -> dict: ...


class ObjWithDictMethodProtocol(Protocol):
    def dict(self) -> dict: ...


DataType: TypeAlias = (dict | ObjWithToPythonMethodProtocol |
                       ObjWithDictMethodProtocol | None)


class JSONLogger(BaseSyncLogger):
    PASS_LEVEL_TO_FORMAT_MESSAGE = "args"
    DEFAULT_MESSAGE_PARTS_SEPARATOR = ":"

    def __init__(
            self,
            name: str | None = None,
            *args: DataType | Exception | str,
            message_parts_separator: str | None = None,
            full_db_objects: bool = False,
    ):
        super().__init__(name)
        self.texts: list[str | Exception] = []
        self.data: list[DataType] = []
        self.set_data(*args)
        self.message_parts_separator = (
                message_parts_separator or
                self.DEFAULT_MESSAGE_PARTS_SEPARATOR
        )
        self.full_db_objects = full_db_objects

    def set_data(self, *default_data: DataType | Exception | str):
        self.texts = [el for el in default_data if isinstance(el, str | Exception)]
        self.data = [el for el in default_data if not isinstance(el, str | Exception)]

    def add_data(self, *data: DataType):
        self.data.extend(data)

    def add_texts(self, *texts: str | Exception):
        self.texts.extend(texts)

    def serialise(self, el: Any, only_dict: bool = False):
        if hasattr(el, "to_python"):
            el = el.to_python()
        elif hasattr(el, "dict") and callable(el.dict):
            el = el.dict()
        elif is_dataclass(el):
            el = asdict(el)

        if el is None:
            return None

        if only_dict and not isinstance(el, dict):
            raise ValueError("only dict or object with to_python() or dict() method")

        if isinstance(el, dict):
            return {str(key): self.serialise(value) for key, value in el.items()}
        if isinstance(el, Iterable) and not isinstance(el, str):
            return [self.serialise(x) for x in el]
        if isinstance(el, datetime):
            return el.isoformat()
        if isinstance(el, time):
            return el.isoformat()
        if isinstance(el, date):
            return el.isoformat()
        if isinstance(el, enum.Enum):
            return el.value
        if isinstance(el, FunctionType):
            return f"Function {el.__name__}"
        if isinstance(el, Exception):
            return repr(el)
        if isinstance(el, Decimal):
            return float(el)
        if isinstance(el, bytes):
            try:
                return el.decode()
            except:
                return str(el)
        return el

    def make_data(self, *args: DataType | str, **kwargs: Any):
        message_parts = [*self.texts]
        log_items = (*self.data, *args, kwargs)
        exception = None
        data = {}

        for item in log_items:
            if isinstance(item, str | Exception):
                if item:
                    message_parts.append(item)
                if isinstance(item, Exception) and not exception:
                    exception = item
                continue

            try:
                item = self.serialise(item, True)
            except Exception as e:
                logging.getLogger("logger.json").critical(
                    f"An error occurred while serialising item: "
                    f"{repr(e)}\n{item}\n" +
                    "".join(traceback.format_stack()[:-1]),
                )
                item = str(item)

            if not item:
                continue
            data.update(item)

        message_parts = [
            repr(el) if isinstance(el, Exception) else el
            for el in message_parts
        ]
        return message_parts, data, exception

    def format_message(self, level: str, *args: DataType | str, **kwargs: Any):
        message_parts, data, exception = self.make_data(*args, **kwargs)
        message = self.message_parts_separator.join(message_parts)

        if not message and not data:
            raise ValueError(
                "There is nothing to log. Message, default data and data are empty"
            )

        result_str = json.dumps(data, indent=4, ensure_ascii=False) if data else ""

        if all((message, result_str)):
            formatted_message = "\n".join((message, result_str))
        else:
            formatted_message = message or result_str

        if exception and self.EXC_INFO_ON_ERROR and level in ("error", "critical"):
            return formatted_message, {"exc_info": exception}
        return formatted_message


def data_from_locals(locals_: dict[str, Any]):
    return {
        key: value
        for key, value in locals_.items()
        if not key.startswith("__")
    }
