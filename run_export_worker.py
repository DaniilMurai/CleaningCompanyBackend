import asyncio
import logging

from config import settings
from core.reports.export.worker import export_report_worker
from loggers.setup import setup_logger


async def main():
    setup_logger(
        name=settings.LOGGER_NAME,
        logs_dir=settings.LOGS_DIR,
        file_name="worker.log",
        level=logging.DEBUG,
    )

    await asyncio.create_task(export_report_worker())


if __name__ == '__main__':
    asyncio.run(main())
