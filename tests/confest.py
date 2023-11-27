import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from src.main import app


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app) as client:
        yield client


@pytest.fixture(autouse=True)
async def client_mongodb():
    async with AsyncIOMotorClient(os.getenv("MONGO_DB_TEST")) as client_db:
        yield client_db
