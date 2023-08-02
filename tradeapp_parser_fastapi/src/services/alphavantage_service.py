import datetime

import requests

from src.assets.schemas import Stock, StockRate
from src.config import Config, get_config
from src.db import get_database


class AlphaVantageService:
    config: Config = get_config()
    ALPHA_VANTAGE_DEMO_API_KEY: str = config.ALPHA_VANTAGE_DEMO_API_KEY
    ALPHA_VANTAGE_API_KEY: str = config.ALPHA_VANTAGE_API_KEY
    ALPHA_VANTAGE_URL: str = config.ALPHA_VANTAGE_URL

    async def save_stocks_rate_to_db(self):
        db = await get_database()
        allowed_stocks_list = await self.get_allowed_stocks_list()
        stocks_list_to_save = []
        for stock in allowed_stocks_list:
            response = requests.get(self.ALPHA_VANTAGE_URL.format(
                stock, self.ALPHA_VANTAGE_DEMO_API_KEY
            ))
            stock_data = response.json()['Global Quote']
            stock = StockRate.model_validate(stock_data).model_dump()
            stocks_list_to_save.append(stock)

        if stocks_list_to_save:
            await db.save_items(model=StockRate, items=stocks_list_to_save)

    @staticmethod
    async def get_allowed_stocks_list():
        db = await get_database()
        allowed_stocks = await db.get_items(model=Stock)
        allowed_stocks_list = [item.stock for item in allowed_stocks]
        return allowed_stocks_list


