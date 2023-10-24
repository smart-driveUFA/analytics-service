import os

from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    def __init__(self):
        self.__client_mongo = AsyncIOMotorClient(os.getenv("MONGO_DB"))
        self.db = self.__client_mongo.api  # database

    async def insert_one(self, name_db: str, obj: dict):
        result = await self.db[name_db].insert_one(obj)
        return result.inserted_id


client_mongo = Mongo()
