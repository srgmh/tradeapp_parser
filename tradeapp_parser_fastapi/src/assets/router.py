from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.assets.schemas import Coin
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


@router.get('/get_coins')
async def get_coins(
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    coins = await db_client.get_items(
        model=Coin,
    )
    return coins


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


@router.delete('/delete_coin/{coin_name}')
async def delete_coin(
    coin_name: str,
    db_client: DatabaseInterface = Depends(MongoDBClient)
):
    # Check if the coin with the given name exists
    if not await db_client.item_exists(model=Coin, query={"coin": coin_name}):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coin with this name not found.",
        )

    # Delete the coin from the database
    if await db_client.delete_item(model=Coin, query={"coin": coin_name}):
        return {"message": "Coin deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete coin.",
        )
