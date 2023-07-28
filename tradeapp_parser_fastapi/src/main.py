import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.assets.router import router as assets_router
from src.db.mongo_db_client import MongoDBClient
from src.periodic_tasks.tasks import get_coins_exchange_rate_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDBClient().get_client()
    asyncio.create_task(get_coins_exchange_rate_task())
    yield
    await MongoDBClient().close_client()

app = FastAPI(lifespan=lifespan)

app.include_router(assets_router)
