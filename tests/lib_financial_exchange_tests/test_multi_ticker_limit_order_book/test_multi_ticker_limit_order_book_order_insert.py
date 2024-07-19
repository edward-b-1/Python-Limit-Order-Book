
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import TopOfBook
from lib_financial_exchange.data_structures.multi_ticker_limit_order_book import MultiTickerLimitOrderBook

from datetime import datetime


# TODO: test the timestamps
def test_multi_limit_order_book_order_insert():

    # Book Setup:
    #
    # Bids:
    # - price=1020, volume=20 (a)
    # - price=1000, volume=10 (b)
    # - price=500, volume=1000
    #
    # Offer:
    # - price=990, volume=100
    #
    # This should produce matches @ price=990
    # a matches first, followed by b

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')
    timestamp = datetime(year=2024, month=7, day=19)
    timestamp_trade = timestamp

    ####

    order_no_match = Order(
        order_id=OrderId(1000),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(1000),
    )
    trades = lob.trade(order_no_match, timestamp=timestamp_trade)
    lob.insert(order_no_match)

    ####

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    trades = lob.trade(order_1, timestamp=timestamp_trade)
    lob.insert(order_1)

    ####

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1020),
        volume=Volume(20),
    )
    trades = lob.trade(order_2, timestamp=timestamp_trade)
    lob.insert(order_2)

    ####

    order_3 = Order(
        order_id=OrderId(3),
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(990),
        volume=Volume(100),
    )
    trades = lob.trade(order_3, timestamp=timestamp_trade)
    lob.insert(order_3)

    trade_1 = Trade(
        order_id_maker=OrderId(2),
        order_id_taker=OrderId(3),
        timestamp=timestamp_trade,
        ticker=ticker,
        int_price=IntPrice(990),
        volume=Volume(20),
    )

    trade_2 = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(3),
        timestamp=timestamp_trade,
        ticker=ticker,
        int_price=IntPrice(990),
        volume=Volume(10),
    )

    assert trades == [ trade_1, trade_2 ]

    assert order_3 == Order(
        order_id=OrderId(3),
        ticker=ticker,
        timestamp=timestamp,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(990),
        volume=Volume(70),
    )
