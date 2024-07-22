
import pytest

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.limit_order_book.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook

from datetime import datetime


def test_single_side_limit_order_book():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    timestamp = datetime(year=2024, month=7, day=19)

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(120),
        volume=Volume(12),
    )

    lob.insert(order_1)
    lob.insert(order_2)

    assert lob.order_id_exists(OrderId(1))
    assert lob.order_id_exists(OrderId(2))
    assert lob.order_id_exists(OrderId(3)) == False

    assert lob.cancel(OrderId(1)) == order_1
    assert lob.cancel(OrderId(2)) == order_2


def test_single_side_limit_order_book_cancel_without_previous_order():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )
    lob.cancel(order_id=OrderId(1))
