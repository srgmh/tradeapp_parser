import asyncio

from fastapi import FastAPI

from src.assets.router import router as assets_router
from src.config import get_config
from src.db import db
from src.periodic_tasks import binance_websocket
from src.periodic_tasks.tasks import get_coins_exchange_rate_task

app = FastAPI(title='Trade Application Parser')
app.include_router(assets_router)


@app.on_event("startup")
async def startup():
    config = get_config()
    await db.connect_to_database(
        path=config.DATABASE_URL,
        database=config.MONGO_INITDB_DATABASE
    )
    await binance_websocket.connect()
    asyncio.create_task(get_coins_exchange_rate_task())


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()
    await binance_websocket.disconnect()


# import asyncio
# from contextlib import asynccontextmanager
#
# from fastapi import FastAPI
#
# from src.assets.router import router as assets_router
# from src.db.mongo_db_client import MongoDBClient
# from src.periodic_tasks.tasks import get_coins_exchange_rate_task
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await MongoDBClient().get_client()
#     asyncio.create_task(get_coins_exchange_rate_task())
#     yield
#     await MongoDBClient().close_client()
#
# app = FastAPI(title='Trade Application Parser', lifespan=lifespan)
# app.include_router(assets_router)
