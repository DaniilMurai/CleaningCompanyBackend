# app/main.py
from fastapi import FastAPI

from app.core.config import settings
from app.router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello, async world!"}


@app.get("/url")
async def root():
    return {"message": settings.DATABASE_URL}
