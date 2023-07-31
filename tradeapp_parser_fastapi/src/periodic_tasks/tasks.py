import asyncio

from src.config import get_config
from src.periodic_tasks import binance_websocket


async def get_coins_exchange_rate_task():
    config = get_config()

    while True:
        await binance_websocket.download_coins_data()
        await asyncio.sleep(config.GETTING_COINS_EXCHANGE_RATE_TASK_TIMEOUT)
