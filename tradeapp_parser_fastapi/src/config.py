from functools import lru_cache

from pydantic.v1.env_settings import BaseSettings


class Config(BaseSettings):

    # Mongo
    MONGO_INITDB_DATABASE: str
    DATABASE_URL: str

    # Binance
    BINANCE_WEBSOCKET_URI: str

    # Periodic tasks timeouts
    GETTING_COINS_RATE_TASK_TIMEOUT: int = 60
    GETTING_STOCKS_RATE_TASK_TIMEOUT: int = 60

    # Alpha Vantage
    ALPHA_VANTAGE_DEMO_API_KEY: str
    ALPHA_VANTAGE_API_KEY: str
    ALPHA_VANTAGE_URL: str

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Config()
