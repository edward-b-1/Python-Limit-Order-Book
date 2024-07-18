
from lib_financial_exchange.financial_exchange_types import ClientName
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import TopOfBook
from lib_financial_exchange.limit_order_book import LimitOrderBook

from datetime import datetime


def test_limit_order_book_trade_insert_new():

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

    lob = LimitOrderBook()
    ticker = Ticker('PYTH')
    client_name = ClientName(client_name='test')
    timestamp = datetime(year=2024, month=7, day=11)

    ####

    order_no_match = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(500),
        volume=Volume(1000),
    )
    (order_id_1, trades) = lob.order_insert(order_no_match)
    assert trades == []

    ####

    order_1 = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )
    (order_id_2, trades) = lob.order_insert(order_1)
    assert trades == []

    ####

    order_2 = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(1020),
        volume=Volume(20),
    )
    (order_id_3, trades) = lob.order_insert(order_2)
    assert trades == []

    ####

    order_3 = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(990),
        volume=Volume(100),
    )
    (order_id_4, trades) = lob.order_insert(order_3)

    assert trades == [
        Trade(order_id_maker=order_id_3, order_id_taker=order_id_4, ticker=ticker, int_price=IntPrice(990), volume=Volume(20)),
        Trade(order_id_maker=order_id_2, order_id_taker=order_id_4, ticker=ticker, int_price=IntPrice(990), volume=Volume(10)),
    ]
    order_3_internal = lob.order_cancel(order_id=order_id_4)
    assert order_3_internal == Order(order_id=order_id_4, ticker=ticker, order_side=OrderSide("SELL"), int_price=IntPrice(990), volume=Volume(70))
