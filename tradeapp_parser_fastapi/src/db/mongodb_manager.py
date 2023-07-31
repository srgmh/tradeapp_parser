import datetime
from typing import List, Type

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel

from src.db import DatabaseManager


class MongoManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(
            self,
            path: str,
            database: str
    ) -> None:
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client[database]

    async def close_database_connection(self) -> None:
        self.client.close()

    async def save_item(
            self,
            item: BaseModel
    ) -> None:
        collection = self.db[item.Meta.collection]
        await collection.insert_one(item.model_dump())

    async def save_items(
            self,
            items: List[dict],
            model: BaseModel
    ) -> None:
        current_datetime = datetime.datetime.now()
        for item in items:
            item['date'] = current_datetime

        collection = self.db[model.Meta.collection]
        await collection.insert_many(items)

    async def get_items(
            self,
            model: Type[BaseModel]
    ) -> List[BaseModel]:
        collection = self.db[model.Meta.collection]
        items_list = []
        items_q = collection.find()
        async for item in items_q:
            items_list.append(model(**item))
        return items_list

    async def item_exists(
            self,
            model: Type[BaseModel],
            query: dict
    ) -> bool:
        collection = self.db[model.Meta.collection]
        result = await collection.find_one(query)
        return result is not None

    async def update_item(
            self,
            model: Type[BaseModel],
            query: dict,
            updates: dict
    ) -> None:
        collection = self.db[model.Meta.collection]
        await collection.update_one(query, {"$set": updates})

    async def delete_item(
            self,
            model: Type[BaseModel],
            query: dict
    ) -> None:
        collection = self.db[model.Meta.collection]
        await collection.delete_one(query)
