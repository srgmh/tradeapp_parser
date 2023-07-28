import asyncio

from src.config import settings
from src.db.mongo_db_client import MongoDBClient
from src.services.asset_service import AssetService


async def get_coins_exchange_rate_task():
    while True:
        await AssetService(MongoDBClient()).save_coins_rate_to_db()
        await asyncio.sleep(settings.GETTING_COINS_EXCHANGE_RATE_TASK_TIMEOUT)
