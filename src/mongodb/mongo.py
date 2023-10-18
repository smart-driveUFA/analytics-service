from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    def __init__(self):
        self.__client_mongo = AsyncIOMotorClient("mongodb://localhost:25017")
        self.__mongo_client = self.__client_mongo.database
        self.collection = self.__mongo_client.collections
