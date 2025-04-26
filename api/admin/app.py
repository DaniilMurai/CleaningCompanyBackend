from fastapi import FastAPI

from .router import router

app = FastAPI(
    title="Neuer Standard Admin API"
)

app.include_router(router)
