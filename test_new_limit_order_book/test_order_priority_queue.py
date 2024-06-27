
import pytest

from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.types.int_price import IntPrice
from new_limit_order_book.types.volume import Volume
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.order import Order
from new_limit_order_book.order_priority_queue import OrderPriorityQueue


def test_order_priority_queue():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(20),
    )

    queue.insert(order_1)
    queue.insert(order_2)

    assert queue.order_id_exists(OrderId(1))
    assert queue.order_id_exists(OrderId(2))
    assert queue.order_id_exists(OrderId(3)) == False

    assert queue.cancel(OrderId(1)) == order_1
    assert queue.cancel(OrderId(2)) == order_2


def test_order_priority_queue_update():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_original = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_updated = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(20),
    )

    queue.insert(order_original)
    queue.update(order_updated)

    assert queue.order_id_exists(OrderId(1))
    assert queue.order_id_exists(OrderId(2)) == False
    assert queue.order_id_exists(OrderId(3)) == False


def test_order_priority_queue_cancel():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(20),
    )

    queue.insert(order_1)
    queue.insert(order_2)

    order_2_cancelled = queue.cancel(OrderId(2))

    assert queue.order_id_exists(OrderId(1))
    assert queue.order_id_exists(OrderId(2)) == False
    assert queue.order_id_exists(OrderId(3)) == False

    assert order_2_cancelled == order_2


def test_order_priority_queue_double_insert_raises():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(20),
    )

    queue.insert(order_1)
    with pytest.raises(Exception):
        queue.insert(order_2)


def test_order_priority_queue_insert_cancel_sequence():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(20),
    )

    queue.insert(order_1)
    queue.cancel(order_1.to_order_id())
    queue.insert(order_1)
    queue.insert(order_2)
    queue.cancel(order_1.to_order_id())
    queue.insert(order_1)

