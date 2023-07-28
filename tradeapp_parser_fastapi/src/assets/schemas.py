import datetime

from pydantic import BaseModel, Field


class CoinRate(BaseModel):
    symbol: str = Field(alias='s')
    last_price: str = Field(alias='c')

    class Meta:
        collection = 'coins_rates'


class Coin(BaseModel):
    coin: str

    class Meta:
        collection = 'coins'


class Stock(BaseModel):
    stock: str

    class Meta:
        collection = 'stocks'
