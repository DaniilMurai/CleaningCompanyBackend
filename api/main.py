import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from db.models import create_tables
from loggers.setup import setup_logger
from utils.api import setup_uvicorn_loggers
from . import admin, auth, users
from .base.exception_handlers import register_general_exception_handlers
from .middlewares.db import db_middleware


@asynccontextmanager
async def lifespan(_):
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
    yield


app = FastAPI(
    title="Neuer Standard API",
    lifespan=lifespan,
)

app.mount("/auth", auth.app)
app.mount("/admin", admin.app)
app.mount("/users", users.app)
app.add_middleware(BaseHTTPMiddleware, dispatch=db_middleware)

register_general_exception_handlers(app)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, async world!"}


@app.get("/health", tags=["status"])
async def health() -> str:
    return "OK"
