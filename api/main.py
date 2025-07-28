import logging
from contextlib import asynccontextmanager

import i18n
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from starlette.middleware.base import BaseHTTPMiddleware

import exceptions
from config import settings
from db.models import create_tables
from loggers.setup import setup_logger
from utils.api import setup_uvicorn_loggers
from utils.init_i18n import init_i18n
from . import admin, auth, client, users
from .base.exception_handlers import register_general_exception_handlers
from .custom_fastapi import CustomFastApi
from .depends.lang import get_lang
from .middlewares.db import db_middleware
from .scheduler import start_daily_assignment_scheduler


@asynccontextmanager
async def lifespan(_):
    init_i18n()
    await create_tables()
    setup_logger(
        name=settings.LOGGER_NAME,
        logs_dir=settings.LOGS_DIR,
        file_name="api.log",
        level=logging.DEBUG,
    )
    setup_uvicorn_loggers(
        logs_dir=settings.LOGS_DIR,
        file_name="api.log",
    )

    await start_daily_assignment_scheduler()

    # asyncio.create_task(export_report_worker())

    yield


app = CustomFastApi(
    title="Neuer Standard API",
    lifespan=lifespan,
    dependencies=[Depends(get_lang)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL
    ],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"]
)

app.mount("/auth", auth.app)
app.mount("/admin", admin.app)
app.mount("/users", users.app)
app.mount("/client", client.app)

app.add_middleware(BaseHTTPMiddleware, dispatch=db_middleware)

register_general_exception_handlers(app)


@app.get("/")
async def root(lang: str = Depends(get_lang)) -> dict[str, str]:
    return {"message": i18n.t("hello world", locale=lang)}


@app.post("/error")
async def test_error(data: dict | None = None):
    raise exceptions.TestError(data)


@app.get("/health", tags=["status"])
async def health() -> str:
    return "OK"
