from fastapi import FastAPI

from .router import router
from ..base.exception_handlers import register_general_exception_handlers

app = FastAPI(
    title="Neuer Standard Auth API",
)

app.include_router(router)

register_general_exception_handlers(app)
