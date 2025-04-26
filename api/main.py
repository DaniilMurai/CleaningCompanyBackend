from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.models import create_tables
from . import admin, auth


@asynccontextmanager
async def lifespan(_):
    await create_tables()
    yield


app = FastAPI(
    title="Neuer Standard API",
    lifespan=lifespan,
)

app.mount("/auth", auth.app)
app.mount("/admin", admin.app)


@app.get("/")
async def root():
    return {"message": "Hello, async world!"}


@app.get("/health", tags=["status"])
async def health():
    return "OK"
