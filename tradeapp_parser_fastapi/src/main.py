from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.assets.router import router as assets_router
from src.db.mongo_db_client import MongoDBClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDBClient().get_client()
    yield
    await MongoDBClient().close_client()

app = FastAPI(lifespan=lifespan)

app.include_router(assets_router)
