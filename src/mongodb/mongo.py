import os

from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    def __init__(self):
        self.__client_mongo = AsyncIOMotorClient(os.getenv("MONGO_DB"))
        self.db = self.__client_mongo.smart_drive  # name of database


client_mongo = Mongo().db
