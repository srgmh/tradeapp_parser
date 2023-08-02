import asyncio

from src.config import get_config
from src.periodic_tasks import binance_websocket
from src.services.alphavantage_service import AlphaVantageService

config = get_config()


async def get_coins_rate_task():
    await binance_websocket.connect()
    while True:
        await binance_websocket.save_coins_rate_to_db()
        await asyncio.sleep(config.GETTING_COINS_RATE_TASK_TIMEOUT)


async def get_stocks_rate_task():
    while True:
        await AlphaVantageService().save_stocks_rate_to_db()
        await asyncio.sleep(config.GETTING_STOCKS_RATE_TASK_TIMEOUT)
