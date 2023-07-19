from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from src.database import close_database_connection, \
    connect_database, get_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database(get_database())
    yield
    await close_database_connection(get_database())

app = FastAPI(lifespan=lifespan)


@app.get('/')
async def post_some(db=Depends(get_database)):
    db = db['tradeapp_fastapi']
    await db.insert_one({'name': 'hello'})
