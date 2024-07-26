
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import TradeId
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from lib_webserver.webserver_types import FastAPI_Trade

from lib_webserver.convert_trades_to_fastapi_trades import convert_trades_to_fastapi_trades

from lib_datetime import datetime_to_order_board_display_string

from datetime import datetime
from datetime import timezone


def test_convert_trades_to_fastapi_trades():

    timestamp = datetime(
        year=2024, month=7, day=19,
        tzinfo=timezone.utc,
    )

    timestamp_str = datetime_to_order_board_display_string(
        now=timestamp,
    )

    trades = [
        Trade(
            trade_id=TradeId(1),
            timestamp=timestamp,
            order_id_maker=OrderId(1),
            order_id_taker=OrderId(2),
            ticker=Ticker('PYTH'),
            int_price=IntPrice(1000),
            volume=Volume(10),
        ),
        Trade(
            trade_id=TradeId(2),
            timestamp=timestamp,
            order_id_maker=OrderId(3),
            order_id_taker=OrderId(4),
            ticker=Ticker('CPP'),
            int_price=IntPrice(1010),
            volume=Volume(12),
        ),
        Trade(
            trade_id=TradeId(3),
            timestamp=timestamp,
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
            trade_id=1,
            timestamp=timestamp_str,
            order_id_maker=1,
            order_id_taker=2,
            ticker='PYTH',
            price=1000,
            volume=10,
        ),
        FastAPI_Trade(
            trade_id=2,
            timestamp=timestamp_str,
            order_id_maker=3,
            order_id_taker=4,
            ticker='CPP',
            price=1010,
            volume=12,
        ),
        FastAPI_Trade(
            trade_id=3,
            timestamp=timestamp_str,
            order_id_maker=5,
            order_id_taker=6,
            ticker='RUST',
            price=2000,
            volume=20,
        ),
    ]
