import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Callable

default_formatter = logging.Formatter(
    "%(asctime)s -%(name)s %(levelname)-8s  - %(message)s",
    "%d.%m.%Y %H:%M:%S"
)


def setup_logger(
        *,
        name: str = None,
        logs_dir: str | None = None,
        file_name: str | None = None,
        formatter: logging.Formatter | Callable[
            ..., logging.Formatter] = default_formatter,
        level = logging.WARNING,
        max_bytes: int = 20000,
        backup_count: int = 1,
        propagate: bool = False,
        file_handler: bool = True,
        stream_handler: bool = True,
        handlers_levels: dict[str, int] | None = None,
        handlers_formatters: dict[str, logging.Formatter | Callable[
            ..., logging.Formatter]] | None = None,
):
    if handlers_levels is None:
        handlers_levels = {}

    if handlers_formatters is None:
        handlers_formatters = {}

    def get_formatter(handler_name: str):
        handler_formatter = handlers_formatters.get(handler_name, formatter)
        if not isinstance(handler_formatter, logging.Formatter):
            handler_formatter = handler_formatter()
        return handler_formatter

    if not isinstance(formatter, logging.Formatter):
        formatter = formatter()

    if logs_dir and not os.path.exists(logs_dir):
        os.makedirs(logs_dir, exist_ok=True)

    handlers = []

    if file_handler and file_name:
        file_path = os.path.join(logs_dir, file_name)
        rh = RotatingFileHandler(
            file_path, maxBytes=max_bytes, backupCount=backup_count
        )
        rh.setFormatter(get_formatter("file"))
        rh.setLevel(handlers_levels.get("file", level))
        handlers.append(rh)

    if stream_handler:
        ch = logging.StreamHandler()
        ch.setFormatter(get_formatter("stream"))
        ch.setLevel(handlers_levels.get("stream", level))
        handlers.append(ch)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    [logger.addHandler(handler) for handler in handlers]

    logger.propagate = propagate

    if not name:
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=handlers,
        )

    return logger
