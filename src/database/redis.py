import json
import os

import aioredis
from aioredis.client import ExpiryT, KeyT
from aioredis.connection import EncodableT


class Redis:
    def __init__(self):
        self.redis_client = aioredis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            db=0,
            decode_responses=True,
        )

    async def get(self, name: KeyT):
        data = await self.redis_client.get(name=name)
        if data:
            return json.loads(data)
        return None

    async def set(
        self,
        name: KeyT,
        value: EncodableT,
        lifetime: ExpiryT = 120,
    ):
        value = json.dumps(value)
        await self.redis_client.set(name=name, value=value, ex=lifetime)

    async def delete(self, name: KeyT):
        await self.redis_client.delete(name)


redis_client = Redis()
