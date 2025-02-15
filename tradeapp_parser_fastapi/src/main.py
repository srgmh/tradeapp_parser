import asyncio

from fastapi import FastAPI

from src.assets.router import router as assets_router
from src.config import get_config
from src.db import db
from src.periodic_tasks import binance_websocket
from src.periodic_tasks.tasks import get_coins_rate_task, get_stocks_rate_task

app = FastAPI(title='Trade Application Parser')
app.include_router(assets_router)


@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(
        path=config.DATABASE_URL,
        database=config.MONGO_INITDB_DATABASE
    )
    asyncio.create_task(get_coins_rate_task())
    asyncio.create_task(get_stocks_rate_task())


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()
    await binance_websocket.disconnect()
