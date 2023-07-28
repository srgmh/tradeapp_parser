from fastapi import APIRouter

from src.assets.schemas import Coin, Stock
from src.db.mongo_db_client import MongoDBClient
from src.services.asset_service import AssetService

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

asset_service = AssetService(MongoDBClient())


@router.post('/add_coin')
async def add_coin(coin: Coin):
    return await asset_service.add_coin(coin)


@router.post('/add_stock')
async def add_stock(stock: Stock):
    return await asset_service.add_stock(stock)


@router.get('/get_coins')
async def get_coins():
    return await asset_service.get_coins()


@router.get('/get_stocks')
async def get_stocks():
    return await asset_service.get_stocks()


@router.patch('/update_coin/{coin_name}')
async def update_coin(coin_name: str, updates: Coin):
    return await asset_service.update_coin(coin_name, updates)


@router.patch('/update_stock/{stock_name}')
async def update_stock(stock_name: str, updates: Stock):
    return await asset_service.update_stock(stock_name, updates)


@router.delete('/delete_coin/{coin_name}')
async def delete_coin(coin_name: str):
    return await asset_service.delete_coin(coin_name)


@router.delete('/stock/{stock_name}')
async def delete_stock(stock_name: str):
    return await asset_service.delete_stock(stock_name)
