
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.data_structures.multi_ticker_limit_order_book import MultiTickerLimitOrderBook

from datetime import datetime


def test_multi_ticker_limit_order_book_order_board():

    limit_order_book = MultiTickerLimitOrderBook()

    timestamp = datetime(year=2024, month=7, day=20)

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=Ticker('ORDER_1_TICKER'),
        order_side=OrderSide('BUY'),
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
        ticker=Ticker('ORDER_2_TICKER'),
        order_side=OrderSide('SELL'),
        int_price=IntPrice(101),
        volume=Volume(11),
    )

    order_3 = Order(
        order_id=OrderId(3),
        timestamp=timestamp,
        ticker=Ticker('ORDER_3_TICKER'),
        order_side=OrderSide('SELL'),
        int_price=IntPrice(102),
        volume=Volume(12),
    )

    order_4 = Order(
        order_id=OrderId(4),
        timestamp=timestamp,
        ticker=Ticker('ORDER_4_TICKER'),
        order_side=OrderSide('BUY'),
        int_price=IntPrice(102),
        volume=Volume(12),
    )

    limit_order_book.insert(order_4)
    limit_order_book.insert(order_2)
    limit_order_book.insert(order_1)
    limit_order_book.insert(order_3)

    orders = limit_order_book.order_board()

    expected_orders = [order_1, order_2, order_3, order_4]
    assert orders == expected_orders, f'orders={orders}\nexpected_orders={expected_orders}'

