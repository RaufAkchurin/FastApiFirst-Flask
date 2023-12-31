import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app, get_db

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname_test"


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_app(test_client):
    # Проверяем корневой эндпоинт
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

    # Проверяем эндпоинт с параметром
    response = test_client.get("/hello/John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello John"}

    # Создаем канал и проверяем создание
    channel_data = {"name": "Test Channel", "channel_chat_id": "12345678901234"}
    response = test_client.post("/channels/", json=channel_data)
    assert response.status_code == 200
    created_channel = response.json()
    assert created_channel["name"] == channel_data["name"]
    assert created_channel["channel_chat_id"] == channel_data["channel_chat_id"]

    # Получаем список каналов и проверяем, что созданный канал в списке
    response = test_client.get("/channels/")
    assert response.status_code == 200
    channels = response.json()
    assert any(channel["name"] == channel_data["name"] for channel in channels)
