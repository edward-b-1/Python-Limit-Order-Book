

from datetime import datetime

from pydantic import BaseModel


class FastAPI_OrderInsertMessage(BaseModel):
    ticker: str
    order_side: str
    price: int
    volume: int


class FastAPI_OrderUpdateMessage(BaseModel):
    order_id: int
    price: int
    volume: int


class FastAPI_OrderCancelPartialMessage(BaseModel):
    order_id: int
    volume: int


class FastAPI_OrderCancelMessage(BaseModel):
    order_id: int


class FastAPI_TopOfBookMessage(BaseModel):
    ticker: str

