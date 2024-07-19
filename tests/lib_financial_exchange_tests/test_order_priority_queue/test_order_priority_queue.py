
import pytest

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.data_structures.order_priority_queue import OrderPriorityQueue

from datetime import datetime


def test_order_priority_queue():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)
    timestamp = datetime(year=2024, month=7, day=19)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
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
    timestamp = datetime(year=2024, month=7, day=19)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_original = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    queue.insert(order_original)
    queue.update(
        order_id=OrderId(1),
        int_price=int_price,
        volume=Volume(5),
    )

    assert queue.order_id_exists(OrderId(1))
    assert queue.order_id_exists(OrderId(2)) == False
    assert queue.order_id_exists(OrderId(3)) == False


def test_order_priority_queue_cancel():

    ticker = Ticker('AAPL')
    order_side = OrderSide.BUY
    int_price = IntPrice(100)
    timestamp = datetime(year=2024, month=7, day=19)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
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
    timestamp = datetime(year=2024, month=7, day=19)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
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
    timestamp = datetime(year=2024, month=7, day=19)

    queue = OrderPriorityQueue(
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
    )

    order_1 = Order(
        order_id=OrderId(1),
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        timestamp=timestamp,
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

