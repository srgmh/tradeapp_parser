import os
from dotenv import find_dotenv, load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(find_dotenv())


def get_database() -> AsyncIOMotorClient:
    url = os.environ.get('DATABASE_URL')
    client = AsyncIOMotorClient(url)
    return client['tradeapp_fastapi']


async def connect_database(client: AsyncIOMotorClient):
    return client


async def close_database_connection(client: AsyncIOMotorClient):
    client.close()
