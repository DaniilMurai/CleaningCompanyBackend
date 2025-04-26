import asyncio
import logging
import traceback
from abc import ABC, abstractmethod
from typing import Awaitable, Literal

from config import settings
from utils.func import check_function_spec


class BaseSyncLogger(ABC):
    """
    Abstract base class for all logger classes.
    """
    PASS_LEVEL_TO_FORMAT_MESSAGE: Literal["args", "kwargs"] | None = None
    EXC_INFO_ON_ERROR: bool = True

    def __init__(self, name: str | None = None):
        self.name = name

    def get_logger_name(self):
        if not self.name:
            return settings.LOGGER_NAME
        return f"{settings.LOGGER_NAME}.{self.name}"

    @abstractmethod
    def format_message(self, *args, **kwargs) -> str | tuple[str, dict]:
        """
        Format message for logging.
        Kwargs will be passed safe, with spec checked, otherwise, args not.
        Implemented method has to accept all possible positional arguments.

        Troubleshooting
        If you have any errors with arguments
        1) Make sure that implemented method accepts all possible positional arguments.
        2) Make sure you are not passing any arguments as positional and keyword at
        the same time

        @param args: The first argument will always be level with type string
        @param kwargs: All extra kwargs passed to log() method
        @return: The formatted message, that will be written to log
        """
        raise NotImplementedError

    def _prepare_args(self, *args, **kwargs):
        """
        Prepare args for logging.
        @param args: Args, passed to log() method
        @param kwargs: Kwargs, passed to log() method
        @return: Tuple of level, parsed args for format_message() method and
        safe_kwargs for format_message() method
        """
        level, *safe_args = args

        if self.PASS_LEVEL_TO_FORMAT_MESSAGE == "args":
            safe_args = (level, *safe_args)
        elif self.PASS_LEVEL_TO_FORMAT_MESSAGE == "kwargs":
            kwargs = {"level": level, **kwargs}

        safe_kwargs = check_function_spec(self.format_message, kwargs)
        return level, safe_args, safe_kwargs

    def write_log(self, level: str, formatted_message: str, **kwargs):
        """
        Method to write log
        @param level:
        @param formatted_message: Message from format_message() method
        @param kwargs: kwargs, passed to log() method
        @return:
        """
        logger = logging.getLogger(self.get_logger_name())
        log_method = getattr(logger, level)

        exc_info = kwargs.get(
            "exc_info", level in ("error", "critical") and self.EXC_INFO_ON_ERROR
        )
        return log_method(formatted_message, exc_info=exc_info)

    def log(self, *args, **kwargs) -> None:
        try:
            level, safe_args, safe_kwargs = self._prepare_args(*args, **kwargs)
            formatted_message = self.format_message(*safe_args, **safe_kwargs)
            if isinstance(formatted_message, tuple):
                override_kwargs = (
                    formatted_message[1]
                    if len(formatted_message) > 1
                    else None
                )
                formatted_message = formatted_message[0]
            else:
                override_kwargs = None

            if override_kwargs:
                kwargs.update(override_kwargs)
            return self.write_log(
                level, formatted_message, **kwargs,
            )
        except Exception as e:
            logging.getLogger("logger").critical(
                f"An error occurred while writing log message: {repr(e)}\n" +
                "".join(traceback.format_stack()[:-1]),
            )

    def error(self, *args, **kwargs):
        return self.log("error", *args, **kwargs)

    def debug(self, *args, **kwargs):
        return self.log("debug", *args, **kwargs)

    def info(self, *args, **kwargs):
        return self.log("info", *args, **kwargs)


class BaseAsyncLogger(BaseSyncLogger):
    @abstractmethod
    async def format_message(self, *args, **kwargs) -> str:
        raise NotImplementedError

    async def log(self, *args, **kwargs):
        try:
            level, safe_args, safe_kwargs = self._prepare_args(*args, **kwargs)
            formatted_message = await self.format_message(*args, **safe_kwargs)
            res = self.write_log(level, formatted_message, **kwargs)
            if asyncio.iscoroutine(res):
                res = await res
            return res
        except Exception as e:
            logging.getLogger("logger").critical(
                f"An error occurred while writing log message: {repr(e)}\n" +
                "".join(traceback.format_stack()[:-1]),
            )

    def error(self, *args, **kwargs) -> Awaitable[None]:
        return super().error()  # type: ignore

    def debug(self, *args, **kwargs) -> Awaitable[None]:
        return super().debug()  # type: ignore

    def info(self, *args, **kwargs) -> Awaitable[None]:
        return super().info()  # type: ignore
