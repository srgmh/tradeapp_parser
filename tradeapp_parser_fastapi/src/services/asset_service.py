from pydantic import BaseModel
from src.assets.schemas import Coin, Stock
from src.db.database_interface import DatabaseInterface


class AssetService:
    def __init__(self, db_client: DatabaseInterface):
        self.db_client = db_client

    async def add_coin(self, coin: Coin):
        if await self.db_client.item_exists(model=Coin, query={'coin': coin.coin}):
            raise ValueError("Coin with this name already exists.")

        item_id = await self.db_client.save_item(coin)
        coin_data = Coin(**coin.model_dump())
        return {
            'id': item_id,
            'coin_data': coin_data
        }

    async def add_stock(self, stock: Stock):
        if await self.db_client.item_exists(model=Stock, query={'stock': stock.stock}):
            raise ValueError("Stock with this name already exists.")

        item_id = await self.db_client.save_item(stock)
        stock_data = Stock(**stock.model_dump())
        return {
            'id': item_id,
            'stock_data': stock_data
        }

    async def get_coins(self) -> list[BaseModel]:
        return await self.db_client.get_items(model=Coin)

    async def get_stocks(self) -> list[BaseModel]:
        return await self.db_client.get_items(model=Stock)

    async def update_coin(self, coin_name: str, updates: Coin):
        if not await self.db_client.item_exists(model=Coin, query={"coin": coin_name}):
            raise ValueError("Coin with this name not found.")
        if await self.db_client.item_exists(model=Coin, query=updates.model_dump()):
            raise ValueError("Failed to update coin. There is already an existing coin.")

        if await self.db_client.update_item(
                model=Coin,
                query={"coin": coin_name},
                updates=updates.model_dump()
        ):
            return {"message": "Coin updated successfully."}
        else:
            raise ValueError("Failed to update coin.")

    async def update_stock(self, stock_name: str, updates: Stock):
        if not await self.db_client.item_exists(model=Stock, query={"stock": stock_name}):
            raise ValueError("Stock with this name not found.")
        if await self.db_client.item_exists(model=Stock, query=updates.model_dump()):
            raise ValueError("Failed to update stock. There is already an existing stock.")

        if await self.db_client.update_item(
                model=Stock,
                query={"stock": stock_name},
                updates=updates.model_dump()
        ):
            return {"message": "Stock updated successfully."}
        else:
            raise ValueError("Failed to update stock.")

    async def delete_coin(self, coin_name: str):
        if not await self.db_client.item_exists(model=Coin, query={"coin": coin_name}):
            raise ValueError("Coin with this name not found.")
        if await self.db_client.delete_item(model=Coin, query={"coin": coin_name}):
            return {"message": "Coin deleted successfully."}
        else:
            raise ValueError("Failed to delete coin.")

    async def delete_stock(self, stock_name: str):
        if not await self.db_client.item_exists(model=Stock, query={"stock": stock_name}):
            raise ValueError("Stock with this name not found.")
        if await self.db_client.delete_item(model=Stock, query={"stock": stock_name}):
            return {"message": "Stock deleted successfully."}
        else:
            raise ValueError("Failed to delete stock.")
