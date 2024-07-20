
import pytest

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook

from datetime import datetime


def test_single_side_limit_order_book_get_all_orders():

    ticker = Ticker('PYTH')
    order_side = OrderSide('BUY')
    timestamp = datetime(year=2024, month=7, day=20)
    volume = Volume(1)

    limit_order_book = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=volume,
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(110),
        volume=volume,
    )

    order_3 = Order(
        order_id=OrderId(3),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(120),
        volume=volume,
    )

    # NOTE: insertion order does not match OrderId ordering and test passes [OK]
    limit_order_book.insert(order_1)
    limit_order_book.insert(order_3)
    limit_order_book.insert(order_2)

    orders = limit_order_book.get_all_orders()

    expected_orders = [order_1, order_2, order_3]
    assert orders == expected_orders, f'get_all_orders failed: orders={orders}, expected_orders={expected_orders}'


def test_single_side_limit_order_book_get_all_orders_no_orders():

    ticker = Ticker('PYTH')
    order_side = OrderSide('BUY')

    limit_order_book = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    orders = limit_order_book.get_all_orders()

    expected_orders = []
    assert orders == expected_orders, f'get_all_orders failed: orders={orders}, expected_orders={expected_orders}'

