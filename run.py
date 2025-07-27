import uvicorn

from config import settings

if __name__ == "__main__":
    uvicorn.run(
        app="api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
    )
