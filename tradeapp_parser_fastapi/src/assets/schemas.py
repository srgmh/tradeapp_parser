from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CoinRate(BaseModel):
    symbol: str = Field(alias='s')
    price: str = Field(alias='c')
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

    class Meta:
        collection = 'coins_rates'


class StockRate(BaseModel):
    symbol: str = Field(alias='01. symbol')
    price: str = Field(alias='05. price')
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

    class Meta:
        collection = 'stocks_rates'


class Coin(BaseModel):
    coin: str

    class Meta:
        collection = 'coins'


class Stock(BaseModel):
    stock: str

    class Meta:
        collection = 'stocks'
