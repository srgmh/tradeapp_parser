from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.assets.router import router as assets_router
from src.database import (close_database_connection, connect_database,
                          get_database)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database(get_database())
    yield
    await close_database_connection(get_database())

app = FastAPI(lifespan=lifespan)

app.include_router(assets_router)
