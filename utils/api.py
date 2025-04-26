import logging

from uvicorn.logging import AccessFormatter

from config import settings
from loggers.setup import setup_logger


def parse_accept_language(lang: str):
    if len(lang) > 2:
        if "-" in lang:
            lang = lang.split("-", 1)[0].strip()

        if ";" in lang:
            lang = lang.split(";", 1)[0].strip()

        if "," in lang:
            lang = lang.split(",", 1)[0].strip()

    if len(lang) != 2:
        lang = settings.DEFAULT_LANG

    return lang


def setup_uvicorn_loggers(
        logs_dir: str | None = None,
        file_name: str | None = None,
):
    setup_logger(
        name="uvicorn",
        logs_dir=logs_dir,
        file_name=file_name,
        level=logging.INFO,
    )

    setup_logger(
        name="uvicorn.error",
        logs_dir=logs_dir,
        file_name=file_name,
        level=logging.DEBUG,
        max_bytes=5_000_000,
        backup_count=10,
        file_handler=True,
        stream_handler=True,
    )

    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers.clear()

    setup_logger(
        name="uvicorn.access",
        logs_dir=logs_dir,
        file_name="access.log",
        formatter=AccessFormatter(
            fmt="%(levelprefix)s %(asctime)s %(client_addr)s - \"%(request_line)s\" "
                "%(status_code)s",
        ), level=logging.INFO,
        max_bytes=1048576,
        backup_count=10,
        file_handler=True,
        stream_handler=True,
    )
