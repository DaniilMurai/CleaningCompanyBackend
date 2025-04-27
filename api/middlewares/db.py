from starlette.requests import Request

from db.session import async_session


async def db_middleware(request: Request, call_next):
    async with async_session() as db:
        request.state.db = db
        return await call_next(request)
