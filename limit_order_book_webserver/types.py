
from pydantic import BaseModel


class FastAPI_OrderId(BaseModel):
    order_id: int

class FastAPI_Ticker(BaseModel):
    ticker: str

class FastAPI_Order(BaseModel):
    order_id: int
    ticker: str
    order_side: str
    price: int
    volume: int


class FastAPI_OrderWithoutOrderId(BaseModel):
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

class FastAPI_ReturnStatus(BaseModel):
    status: str
    message: str|None = None

class FastAPI_ReturnStatusWithOrder(FastAPI_ReturnStatus):
    order: FastAPI_Order

class FastAPI_ReturnStatusWithTrades(FastAPI_ReturnStatus):
    trades: list[FastAPI_Trade]

class FastAPI_ReturnStatusWithTradesAndOrderId(FastAPI_ReturnStatus):
    order_id: int
    trades: list[FastAPI_Trade]

class FastAPI_ReturnStatusWithTopOfBook(FastAPI_ReturnStatus):
    top_of_book: FastAPI_TopOfBook