from fastapi import Depends
from starlette.requests import Request


async def get_db(request: Request):
    return request.state.db


DBDepend = Depends(get_db)
