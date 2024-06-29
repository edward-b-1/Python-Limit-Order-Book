
import pytest

from limit_order_book.types.order_id import OrderId


def test_order_id_equal():

    order_id_1 = OrderId(1)
    order_id_2 = OrderId(1)
    assert order_id_1 == order_id_2


def test_order_id_not_equal():

    order_id_1 = OrderId(1)
    order_id_2 = OrderId(2)
    assert order_id_1 != order_id_2


def test_order_id_negative():

    with pytest.raises(Exception):
        OrderId(-1)