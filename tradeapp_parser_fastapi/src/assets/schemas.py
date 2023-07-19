from pydantic import BaseModel


class Coin(BaseModel):
    coin: str
