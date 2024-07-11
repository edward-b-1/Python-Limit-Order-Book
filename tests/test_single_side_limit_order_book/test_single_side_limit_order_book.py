
import pytest

from limit_order_book.types import OrderId
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.types import Ticker
from limit_order_book.types import Order
from limit_order_book.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook


def test_single_side_limit_order_book():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY

    lob = SingleSideLimitOrderBook(
        ticker=ticker,
        order_side=order_side,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
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
