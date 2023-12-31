import asyncio
import pytest
import timeit
from fastapi.testclient import TestClient
from httpx import AsyncClient  # Используйте правильный импорт

from main import app

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname_test"


@pytest.fixture
def test_client():
    # TODO тест не работает полность асинхронно
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_rps(test_client):
    async def make_request():
        # Сделать запрос к /channels/
        return test_client.get("/channels/")

    # Количество запросов для измерения
    num_requests = 100

    # Замеряем время выполнения
    tasks = [make_request() for _ in range(num_requests)]
    start_time = timeit.default_timer()
    await asyncio.gather(*tasks)
    execution_time = timeit.default_timer() - start_time

    # Вычисляем RPS
    rps = num_requests / execution_time
    print(f"Requests per second: {rps}")
    assert rps < 1  # Проверяем, что RPS больше 1 (можете подобрать подходящий порог)
