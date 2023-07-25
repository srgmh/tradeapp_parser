from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.assets.schemas import Coin, Stock
from src.db.database_interface import DatabaseInterface
from src.db.mongo_db_client import MongoDBClient

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post('/add_coin')
async def add_coin(
    coin: Coin,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    if await db_client.item_exists(model=Coin, query={'coin': coin.coin}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coin with this name already exists.",
        )

    item_id = await db_client.save_item(coin)
    coin_data = Coin(**coin.model_dump())
    return {
        'id': item_id,
        'coin_data': coin_data
    }


@router.post('/add_stock')
async def add_stock(
    stock: Stock,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    if await db_client.item_exists(model=Stock, query={'stock': stock.stock}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock with this name already exists.",
        )

    item_id = await db_client.save_item(stock)
    stock_data = Stock(**stock.model_dump())
    return {
        'id': item_id,
        'stock_data': stock_data
    }


@router.get('/get_coins')
async def get_coins(
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    coins = await db_client.get_items(
        model=Coin,
    )
    return coins


@router.get('/get_stocks')
async def get_stocks(
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    stocks = await db_client.get_items(
        model=Stock,
    )
    return stocks


@router.patch('/update_coin/{coin_name}')
async def update_coin(
    coin_name: str,
    updates: Coin,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    if not await db_client.item_exists(model=Coin, query={"coin": coin_name}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coin with this name not found.",
        )
    if await db_client.item_exists(model=Coin, query=updates.model_dump()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to update coin. There is already existing coin.",
        )
    if await db_client.update_item(
            model=Coin,
            query={"coin": coin_name},
            updates=updates.model_dump()
    ):
        return {"message": "Coin updated successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update coin.",
        )


@router.patch('/update_stock/{stock_name}')
async def update_stock(
    stock_name: str,
    updates: Stock,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    if not await db_client.item_exists(model=Stock, query={"stock": stock_name}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock with this name not found.",
        )
    if await db_client.item_exists(model=Stock, query=updates.model_dump()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to update stock. There is already existing stock.",
        )
    if await db_client.update_item(
            model=Stock,
            query={"stock": stock_name},
            updates=updates.model_dump()
    ):
        return {"message": "Stock updated successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update stock.",
        )


@router.delete('/delete_coin/{coin_name}')
async def delete_coin(
    coin_name: str,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    if not await db_client.item_exists(model=Coin, query={"coin": coin_name}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coin with this name not found.",
        )
    if await db_client.delete_item(model=Coin, query={"coin": coin_name}):
        return {"message": "Coin deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete coin.",
        )


@router.delete('/stock/{stock_name}')
async def delete_stock(
    stock_name: str,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    if not await db_client.item_exists(model=Stock, query={"stock": stock_name}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock with this name not found.",
        )
    if await db_client.delete_item(model=Stock, query={"stock": stock_name}):
        return {"message": "Stock deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete stock.",
        )
