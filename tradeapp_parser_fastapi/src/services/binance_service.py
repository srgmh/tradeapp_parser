import datetime
import json
from typing import Optional

import websockets
from uvicorn.main import logger

from src.assets.schemas import Coin, CoinRate
from src.config import Config, get_config
from src.db import get_database


class BinanceService:
    config: Config = get_config()
    uri: str = config.BINANCE_WEBSOCKET_URI
    websocket: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        logger.info('Connected to Binance websocket')

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            logger.info('Disconnected Binance websocket')

    async def get_websocket_json_data(self):
        data = await self.websocket.recv()
        data_dict = json.loads(data)
        return data_dict['data']

    async def save_coins_rate_to_db(self):
        db = await get_database()
        coins_set = [item.coin for item in await db.get_items(model=Coin)]
        all_coins_data = await self.get_websocket_json_data()

        if coins_set and all_coins_data:
            items = [CoinRate.model_validate(item).model_dump()
                     for item in all_coins_data if item['s'] in coins_set]
            if items:
                await db.save_items(model=CoinRate, items=items)
