import asyncio

from aiokafka import AIOKafkaProducer
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

@app.post("/send_message_to_kafka/")
async def send_message(topic: str, key: str, value: str):
    producer_config = {
        "bootstrap_servers": "kafka:9092",
    }
    app.producer = AIOKafkaProducer(**producer_config)

    async with app.producer as producer:
        await producer.send_and_wait(topic, key=key.encode(), value=value.encode())

    return {"message": "Сообщение отправлено"}
