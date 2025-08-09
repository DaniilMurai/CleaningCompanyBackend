import os

import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app
from config import settings
from utils.security.tokens import create_access_token, create_refresh_token

BASE_URL = f"http://{settings.HOST}/auth"
USER_DATA = {
    "nickname": os.getenv("TEST_USERNAME"),
    "password": os.getenv("TEST_PASSWORD")
}
ACCESS_TOKEN = create_access_token(USER_DATA)
REFRESH_TOKEN = create_refresh_token(USER_DATA)
access = create_access_token(
    data={"sub": str(user.id), "type": "access"}
)
refresh = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})


# await self.crud.get(
#             nickname=data.nickname,
#             status=schemas.UserStatus.active
#         )

@pytest.mark.anyio()
async def test_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post(url="/login", json=USER_DATA)
    assert response.status_code == 200
    must_have_list = ["access_token", "refresh_token", "token_type"]
    assert all(must_have in response.json() for must_have in must_have_list)
