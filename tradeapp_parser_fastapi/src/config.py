from functools import lru_cache

from pydantic.v1.env_settings import BaseSettings


class Config(BaseSettings):
    MONGO_INITDB_DATABASE: str
    DATABASE_URL: str
    BINANCE_WEBSOCKET_URI: str
    GETTING_COINS_EXCHANGE_RATE_TASK_TIMEOUT: int = 180

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Config()
