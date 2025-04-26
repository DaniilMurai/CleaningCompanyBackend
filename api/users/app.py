from fastapi import FastAPI

from .router import router

app = FastAPI(
    title="Neuer Standard Users API",
)

app.include_router(router)
