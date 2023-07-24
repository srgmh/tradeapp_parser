from typing import Optional, List, Type

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from src.config import mongo_settings
from src.db.database_interface import DatabaseInterface


class MongoDBClient(DatabaseInterface):
    def __init__(self):
        self.mongo_client = None

    async def get_client(self):
        if self.mongo_client is None:
            self.mongo_client = AsyncIOMotorClient(mongo_settings.DATABASE_URL)
        return self.mongo_client

    async def close_client(self):
        if self.mongo_client:
            self.mongo_client.close()
            self.mongo_client = None

    async def save_item(self, item: BaseModel) -> str:
        client = await self.get_client()
        db = client[mongo_settings.MONGO_INITDB_DATABASE]
        collection = db[item.Meta.collection]
        result = await collection.insert_one(item.model_dump())
        return str(result.inserted_id)

    async def get_items(self, model: Type[BaseModel]) -> List[BaseModel]:
        client = await self.get_client()
        db = client[mongo_settings.MONGO_INITDB_DATABASE]
        collection = db[model.Meta.collection]
        cursor = collection.find({})
        items = [model(**item) for item in await cursor.to_list(length=None)]
        return items

    async def item_exists(
            self,
            model: Type[BaseModel],
            query: dict) -> bool:
        client = await self.get_client()
        db = client[mongo_settings.MONGO_INITDB_DATABASE]
        collection = db[model.Meta.collection]
        result = await collection.find_one(query)
        return result is not None

    async def update_item(self, model: Type[BaseModel], query: dict, updates: dict) -> bool:
        client = await self.get_client()
        db = client[mongo_settings.MONGO_INITDB_DATABASE]
        collection = db[model.Meta.collection]

        existing_item = await collection.find_one(query)
        if not existing_item:
            return False

        await collection.update_one(query, {"$set": updates})
        return True

    async def delete_item(self, model: Type[BaseModel], query: dict) -> bool:
        client = await self.get_client()
        db = client[mongo_settings.MONGO_INITDB_DATABASE]
        collection = db[model.Meta.collection]

        existing_item = await collection.find_one(query)
        if not existing_item:
            return False

        await collection.delete_one(query)
        return True
