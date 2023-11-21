import asyncio
from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture(autouse=True, scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app) as client:
        yield client
