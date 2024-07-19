
from lib_financial_exchange.financial_exchange_types.message_types import OrderInsertMessage

from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from datetime import datetime
from datetime import timezone

import pytest


def test_order_insert_message():

    order_insert_message = OrderInsertMessage(
        created_datetime=datetime(year=2024, month=7, day=19, tzinfo=timezone.utc),
        ticker=Ticker('PYTH'),
        order_side=OrderSide('BUY'),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )

    order_insert_message_serialized = (
        f'ORDER_INSERT 2024-07-19T00:00:00.000000+0000 PYTH BUY 1000 10'
    )

    assert str(order_insert_message) == (
        f'OrderInsertMessage(2024-07-19 00:00:00+00:00, Ticker(PYTH), BUY, IntPrice(1000), Volume(10))'
    )

    assert order_insert_message.serialize() == order_insert_message_serialized

    assert OrderInsertMessage.deserialize(order_insert_message_serialized) == order_insert_message


def test_order_insert_message_deserialize_wrong_number_of_fields():

    order_insert_message_serialized = (
        f'ORDER_INSERT 2024-07-19T00:00:00.000000+0000 PYTH BUY 1000 10 10'
    )
    with pytest.raises(AssertionError):
        OrderInsertMessage.deserialize(order_insert_message_serialized)

    order_insert_message_serialized = (
        f'ORDER_INSERT 2024-07-19T00:00:00.000000+0000 PYTH BUY 1000'
    )
    with pytest.raises(AssertionError):
        OrderInsertMessage.deserialize(order_insert_message_serialized)
