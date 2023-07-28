from pydantic.v1.env_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_DATABASE: str
    DATABASE_URL: str

    BINANCE_WEBSOCKET_URI: str = 'wss://stream.binance.com:443/stream?streams=!miniTicker@arr'
    GETTING_COINS_EXCHANGE_RATE_TASK_TIMEOUT: int = 30

    class Config:
        env_file = '.env'


settings = Settings()
