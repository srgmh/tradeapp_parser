from motor.motor_asyncio import AsyncIOMotorClient

from src.config import mongo_settings


def get_database() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(mongo_settings.DATABASE_URL)
    return client[mongo_settings.MONGO_INITDB_DATABASE]


async def connect_database(client: AsyncIOMotorClient):
    return client


async def close_database_connection(client: AsyncIOMotorClient):
    client.close()
