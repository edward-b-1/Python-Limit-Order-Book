
from pydantic import BaseModel

from datetime import datetime


class FastAPI_OrderId(BaseModel):
    order_id: int

class FastAPI_OrderIdVolume(BaseModel):
    order_id: int
    volume: int

class FastAPI_OrderIdPriceVolume(BaseModel):
    order_id: int
    price: int
    volume: int

class FastAPI_Ticker(BaseModel):
    ticker: str

class FastAPI_Order(BaseModel):
    order_id: int
    ticker: str
    order_side: str
    price: int
    volume: int

class FastAPI_Trade(BaseModel):
    order_id_maker: int
    order_id_taker: int
    ticker: str
    price: int
    volume: int

class FastAPI_TopOfBook(BaseModel):
    ticker: str
    price_buy: int|None = None
    volume_buy: int|None = None
    price_sell: int|None = None
    volume_sell: int|None = None

