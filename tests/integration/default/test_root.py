import i18n
import pytest
from httpx import ASGITransport, AsyncClient

from api.depends import lang
from api.main import app
from config import settings


@pytest.mark.anyio()
async def test_health():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url=f"http://{settings.HOST}"
    ) as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == 'OK'


@pytest.mark.anyio()
async def test_root():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url=f"http://{settings.HOST}"
    ) as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": i18n.t("hello world", locale=lang)}
