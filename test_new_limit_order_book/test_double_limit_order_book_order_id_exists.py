
import pytest

from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.types.int_price import IntPrice
from new_limit_order_book.types.volume import Volume
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.order import Order
from new_limit_order_book.double_limit_order_book import DoubleLimitOrderBook


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

