import os

from dotenv import find_dotenv, load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(find_dotenv())


async def get_database() -> AsyncIOMotorClient:
    url = os.environ.get('DATABASE_URL')
    client = AsyncIOMotorClient(url)
    database = os.environ.get('MONGO_INITDB_DATABASE')
    return client[database]
