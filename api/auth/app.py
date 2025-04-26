from fastapi import FastAPI

from .router import router

app = FastAPI(
    title="Neuer Standard Auth API",
)

app.include_router(router)
