
from fastapi import FastAPI
from pydantic import BaseModel

from limit_order_book.limit_order_book_wrapper import LimitOrderBook
from limit_order_book.order import Order
from limit_order_book.trade import Trade
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.order_side import OrderSide
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume

import os
import threading

limit_order_book = LimitOrderBook()


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

class FastAPI_ReturnStatusWithTopOfBook(FastAPI_ReturnStatus):
    top_of_book: FastAPI_TopOfBook


def convert_trades_to_fastapi_trades(trades: list[Trade]) -> list[FastAPI_Trade]:

    def convert_trade(trade: Trade) -> FastAPI_Trade:
        return FastAPI_Trade(
            order_id_maker=trade._order_id_maker,
            order_id_taker=trade._order_id_taker,
            ticker=trade._ticker,
            price=trade._int_price,
            volume=trade._volume,
        )

    fastapi_trades = list(
        map(
            lambda trade: convert_trade(trade),
            trades,
        )
    )
    return fastapi_trades


print(f'__name__={__name__}')
app = FastAPI()

@app.get('/')
def root():
    return {
        'documentation_page:': 'https://github.com/edward-b-1/Python-Limit-Order-Book',
        'message': 'please download the client application from the documentation page to interact with this site'
    }

@app.post('/send_order')
def send_order(fastapi_order: FastAPI_Order):
    print(os.getpid())
    print(threading.get_native_id())
    order = Order(
        order_id=OrderId(fastapi_order.order_id),
        ticker=Ticker(fastapi_order.ticker),
        order_side=OrderSide(value=fastapi_order.order_side),
        int_price=IntPrice(fastapi_order.price),
        volume=Volume(fastapi_order.volume),
    )
    try:
        trades = limit_order_book.order_insert(order)
        fastapi_trades = convert_trades_to_fastapi_trades(trades)
        return FastAPI_ReturnStatusWithTrades(
            status='success',
            message=None,
            trades=fastapi_trades,
        )
    except RuntimeError as error:
        return FastAPI_ReturnStatus(
            status='error',
            message=str(error), # TODO: is this error good enough?
        )

@app.post('/cancel_order')
def cancel_order(fastapi_order_id: FastAPI_OrderId):
    print(os.getpid())
    print(threading.get_native_id())
    order_id = OrderId(fastapi_order_id.order_id)
    order = limit_order_book.order_cancel(order_id)

    if order is None:
        return FastAPI_ReturnStatus(
            status='success',
            message=f'order id {fastapi_order_id.order_id} does not exist, no order to cancel',
        )
    else:
        fastapi_order = FastAPI_Order(
            order_id=order._order_id,
            ticker=order._ticker,
            order_side=order._order_side,
            price=order._int_price,
            volume=order._volume,
        )
        return FastAPI_ReturnStatusWithOrder(
            status='success',
            message=f'order id {fastapi_order_id.order_id} cancelled',
            order=fastapi_order,
        )

@app.post('/modify_order')
def modify_order(fastapi_order: FastAPI_Order):
    print(os.getpid())
    print(threading.get_native_id())
    order = Order(
        order_id=OrderId(fastapi_order.order_id),
        ticker=Ticker(fastapi_order.ticker),
        order_side=OrderSide(value=fastapi_order.order_side),
        int_price=IntPrice(fastapi_order.price),
        volume=Volume(fastapi_order.volume),
    )
    trades = limit_order_book.order_modify(order)
    fastapi_trades = convert_trades_to_fastapi_trades(trades)
    return FastAPI_ReturnStatusWithTrades(
        status='success',
        message=None,
        trades=fastapi_trades,
    )

@app.get('/top_of_book')
def top_of_book(fastapi_ticker: FastAPI_Ticker):
    print(os.getpid())
    print(threading.get_native_id())
    ticker = Ticker(
        ticker=fastapi_ticker.ticker,
    )
    top_of_book = limit_order_book.top_of_book(ticker)

    ticker = top_of_book._ticker.to_str()

    price_buy = top_of_book._int_price_buy
    if price_buy is not None:
        price_buy = price_buy._int_price

    price_sell = top_of_book._int_price_sell
    if price_sell is not None:
        price_sell = price_sell._int_price

    volume_buy = top_of_book._volume_buy
    if volume_buy is not None:
        volume_buy = volume_buy._volume

    volume_sell = top_of_book._volume_sell
    if volume_sell is not None:
        volume_sell = volume_sell._volume

    fastapi_top_of_book = FastAPI_TopOfBook(
        ticker=ticker,
        price_buy=price_buy,
        volume_buy=volume_buy,
        price_sell=price_sell,
        volume_sell=volume_sell,
    )
    r = FastAPI_ReturnStatusWithTopOfBook(
        status='success',
        message=None,
        top_of_book=fastapi_top_of_book,
    )
    print(r)
    return r

@app.get('/ping')
def ping():
    return {
        'status': 'success',
        'message': None,
        'ping': 'pong',
    }


shared_data = None

class FastAPI_Value(BaseModel):
    value: str

@app.post('/put')
def put(value: FastAPI_Value):
    print(f'value={value.value}')
    global shared_data
    shared_data = value
    return {
        'status': 'success',
    }

@app.get('/get')
def get():
    return {
        'shared_data': shared_data,
    }