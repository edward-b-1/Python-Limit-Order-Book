

from lib_webserver.webserver_types.webserver_types import FastAPI_Order
from lib_webserver.webserver_types.webserver_types import FastAPI_Trade
from lib_webserver.webserver_types.webserver_types import FastAPI_TopOfBook


from pydantic import BaseModel

from datetime import datetime


class FastAPI_ReturnStatus(BaseModel):
    status: str
    message: str|None = None

class FastAPI_ReturnStatusWithPing(FastAPI_ReturnStatus):
    ping: str

class FastAPI_ReturnStatusWithOrder(FastAPI_ReturnStatus):
    order: FastAPI_Order

class FastAPI_ReturnStatusWithTrades(FastAPI_ReturnStatus):
    trades: list[FastAPI_Trade]

class FastAPI_ReturnStatusWithTradesAndOrderId(FastAPI_ReturnStatus):
    order_id: int
    trades: list[FastAPI_Trade]

class FastAPI_ReturnStatusWithTopOfBook(FastAPI_ReturnStatus):
    top_of_book: FastAPI_TopOfBook

class FastAPI_ReturnStatusWithOrderBoard(FastAPI_ReturnStatus):
    orders: list[FastAPI_Order]

class FastAPI_ReturnStatusWithTickerList(FastAPI_ReturnStatus):
    tickers: list[str]

