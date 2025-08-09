import os
from typing import Any, AsyncGenerator

import pytest
from dotenv import load_dotenv
from sqlalchemy import and_

from config import settings
from db.models import User
from utils.password import get_password_hash

load_dotenv()
from httpx import ASGITransport, AsyncClient

import exceptions
from db.session import async_session_maker
from utils.security.tokens import create_access_token
from api.main import app


@pytest.fixture(autouse=True)
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
async def access_token() -> str:
    async with async_session_maker as db:
        user = (await db.select(User).where(
            and_(
                User.nickname == os.getenv(
                    "TEST_USERNAME"
                ), User.hashed_password == get_password_hash(
                    os.getenv("TEST_PASSWORD")
                ), User.is_deleted == False
            )
        )).scalars().one_or_none()

        if not user:
            raise exceptions.ObjectNotFoundByIdError("User", -5)
        return create_access_token(data={"sub": str(user.id), "type": "access"})


@pytest.fixture
async def authorized_client(
        access_token: str, base_url: str = f"http://{settings.HOST}"
) -> AsyncGenerator[AsyncClient, Any]:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url=base_url, headers=headers
    ) as ac:
        yield ac
