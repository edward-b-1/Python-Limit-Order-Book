
# import os
# with open('pythonpath.txt', 'w') as ofile:
#     ofile.write(os.environ['PYTHONPATH'])

import pytest

from limit_order_book.types import OrderId
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.types import OrderSide
from limit_order_book.types import Ticker
from limit_order_book.order import Order
from limit_order_book.double_limit_order_book import DoubleLimitOrderBook


def test_double_limit_order_book_order_id_exists():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY

    lob = DoubleLimitOrderBook(
        ticker=ticker,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )

    lob.insert(order_1)

    assert lob.order_id_exists(OrderId(1))
    assert lob.order_id_exists(OrderId(2)) == False

