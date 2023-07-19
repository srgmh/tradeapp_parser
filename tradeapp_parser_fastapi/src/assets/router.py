from fastapi import APIRouter, Depends, HTTPException

from src.assets.schemas import Coin
from src.database import get_database

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post('/add_coin')
async def add_coin(coin: Coin, db=Depends(get_database)):
    collection = db['coins']

    existing_coin = await collection.find_one({"coin": coin.coin})
    if existing_coin:
        raise HTTPException(status_code=400, detail="Coin already exists")

    coin_dict = coin.model_dump()
    await collection.insert_one(coin_dict)
    return {
        'success': True,
        'message': 'Coin added'
    }
