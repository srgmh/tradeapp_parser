from pydantic import BaseModel, Field


class Coin(BaseModel):
    coin: str

    class Meta:
        collection = 'coins'
