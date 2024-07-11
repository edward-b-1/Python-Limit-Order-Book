
from limit_order_book_webserver.convert_trades_to_fastapi_trades import convert_trades_to_fastapi_trades
from limit_order_book_webserver.webserver import FastAPI_Trade
from limit_order_book.trade import Trade
from limit_order_book.types import OrderId
from limit_order_book.types import Ticker
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume


def test_convert_trades_to_fastapi_trades():

    trades = [
        Trade(
            order_id_maker=OrderId(1),
            order_id_taker=OrderId(2),
            ticker=Ticker('PYTH'),
            int_price=IntPrice(1000),
            volume=Volume(10),
        ),
        Trade(
            order_id_maker=OrderId(3),
            order_id_taker=OrderId(4),
            ticker=Ticker('CPP'),
            int_price=IntPrice(1010),
            volume=Volume(12),
        ),
        Trade(
            order_id_maker=OrderId(5),
            order_id_taker=OrderId(6),
            ticker=Ticker('RUST'),
            int_price=IntPrice(2000),
            volume=Volume(20),
        ),
    ]

    fast_api_trades = convert_trades_to_fastapi_trades(trades)

    assert fast_api_trades == [
        FastAPI_Trade(
            order_id_maker=1,
            order_id_taker=2,
            ticker='PYTH',
            price=1000,
            volume=10,
        ),
        FastAPI_Trade(
            order_id_maker=3,
            order_id_taker=4,
            ticker='CPP',
            price=1010,
            volume=12,
        ),
        FastAPI_Trade(
            order_id_maker=5,
            order_id_taker=6,
            ticker='RUST',
            price=2000,
            volume=20,
        ),
    ]
