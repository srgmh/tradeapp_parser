from fastapi import APIRouter, Depends

from src.assets.schemas import Coin, Stock
from src.db import DatabaseManager, get_database

router = APIRouter()


@router.post('/add_coin')
async def add_stock(
        coin: Coin,
        db: DatabaseManager = Depends(get_database)
):
    return await db.save_item(coin)


@router.post('/add_stock')
async def add_stock(
        stock: Stock,
        db: DatabaseManager = Depends(get_database)
):
    return await db.save_item(stock)


@router.get('/get_coins')
async def get_coins(
        db: DatabaseManager = Depends(get_database)
):
    return await db.get_items(model=Coin)


@router.get('/get_stocks')
async def get_stocks(
        db: DatabaseManager = Depends(get_database)
):
    return await db.get_items(model=Stock)


@router.patch('/update_coin/{coin_name}')
async def update_coin(
        coin_name: str,
        updates: Coin,
        db: DatabaseManager = Depends(get_database)
):
    await db.update_item(
        model=Coin,
        query={'coin': coin_name},
        updates=updates.model_dump()
    )


@router.patch('/update_stock/{stock_name}')
async def update_coin(
        stock_name: str,
        updates: Stock,
        db: DatabaseManager = Depends(get_database)
):
    await db.update_item(
        model=Stock,
        query={'stock': stock_name},
        updates=updates.model_dump()
    )


@router.delete('/delete_coin/{coin_name}')
async def delete_coin(
        coin_name: str,
        db: DatabaseManager = Depends(get_database)
):
    await db.delete_item(
        model=Coin,
        query={'coin': coin_name}
    )


@router.delete('/stock/{stock_name}')
async def delete_stock(
        stock_name: str,
        db: DatabaseManager = Depends(get_database)
):
    await db.delete_item(
        model=Stock,
        query={'stock': stock_name}
    )
