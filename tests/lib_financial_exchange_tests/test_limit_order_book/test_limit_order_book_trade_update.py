
from lib_financial_exchange.financial_exchange_types import TradeId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.limit_order_book import LimitOrderBook

from datetime import datetime


def test_limit_order_book_order_update():

    # Book Setup:
    #
    # Bids:
    # - price=1020, volume=20 (a)
    # - price=1000, volume=10 (b)
    # - price=500, volume=1000
    #
    # Offer:
    # - price=1100, volume=100 (initially)
    # - price=990, volume=100 (changes to)
    #
    # This should produce matches @ price=990
    # a matches first, followed by b

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=11)

    ####

    order_no_match = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(1000),
    )
    (order_id_order_no_match, trades) = lob.order_insert(
        order_no_match.to_ticker(),
        order_no_match.to_order_side(),
        order_no_match.to_int_price(),
        order_no_match.to_volume(),
        order_no_match.to_timestamp(),
    )
    assert trades == []

    ####

    order_1 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    (order_id_1, trades) = lob.order_insert(
        order_1.to_ticker(),
        order_1.to_order_side(),
        order_1.to_int_price(),
        order_1.to_volume(),
        order_1.to_timestamp(),
    )
    assert trades == []

    ####

    order_2 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1020),
        volume=Volume(20),
    )
    (order_id_2, trades) = lob.order_insert(
        order_2.to_ticker(),
        order_2.to_order_side(),
        order_2.to_int_price(),
        order_2.to_volume(),
        order_2.to_timestamp(),
    )
    assert trades == []

    ####

    order_3 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(1100),
        volume=Volume(100),
    )
    (order_id_3, trades) = lob.order_insert(
        order_3.to_ticker(),
        order_3.to_order_side(),
        order_3.to_int_price(),
        order_3.to_volume(),
        order_3.to_timestamp(),
    )
    assert trades == []

    trades = lob.order_update(
        order_id=order_id_3,
        int_price=IntPrice(980),
        volume=Volume(100),
        timestamp=timestamp,
    )

    assert trades == [
        Trade(
            trade_id=TradeId(1),
            order_id_maker=order_id_2,
            order_id_taker=order_id_3,
            timestamp=timestamp,
            ticker=ticker,
            int_price=IntPrice(980),
            volume=Volume(20),
        ),
        Trade(
            trade_id=TradeId(2),
            order_id_maker=order_id_1,
            order_id_taker=order_id_3,
            timestamp=timestamp,
            ticker=ticker,
            int_price=IntPrice(980),
            volume=Volume(10),
        ),
    ]

    order_id_3_remaining = lob.order_cancel(order_id_3)
    assert order_id_3_remaining == Order(
        order_id=order_id_3,
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(980),
        volume=Volume(70),
    )
