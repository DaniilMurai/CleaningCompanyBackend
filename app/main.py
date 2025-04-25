# app/main.py
from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.router import router

app = FastAPI()

app.include_router(router)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Запускаем создание таблиц при старте
@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello, async world!"}


@app.get("/url")
async def root():
    return {"message": settings.DATABASE_URL}
