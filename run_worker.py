import asyncio

from core.reports.export.worker import export_report_worker


async def main():
    await asyncio.create_task(export_report_worker())


if __name__ == '__main__':
    asyncio.run(main())
