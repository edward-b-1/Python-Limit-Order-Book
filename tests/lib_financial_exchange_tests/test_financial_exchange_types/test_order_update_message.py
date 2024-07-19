
from lib_financial_exchange.financial_exchange_types.message_types import OrderUpdateMessage

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from datetime import datetime
from datetime import timezone

import pytest


def test_order_update_message():

    order_update_message = OrderUpdateMessage(
        created_datetime=datetime(year=2024, month=7, day=19, tzinfo=timezone.utc),
        order_id=OrderId(1),
        int_price=IntPrice(1000),
        volume=Volume(10),
    )

    order_update_message_serialized = (
        f'ORDER_UPDATE 2024-07-19T00:00:00.000000+0000 1 1000 10'
    )

    assert str(order_update_message) == (
        f'OrderUpdateMessage(2024-07-19 00:00:00+00:00, OrderId(1), IntPrice(1000), Volume(10))'
    )

    assert order_update_message.serialize() == order_update_message_serialized

    assert OrderUpdateMessage.deserialize(order_update_message_serialized) == order_update_message


def test_order_update_message_deserialize_wrong_number_of_fields():

    order_update_message_serialized_1 = (
        f'ORDER_UPDATE 2024-07-19T00:00:00.000000+0000 1 1000 10 10'
    )
    with pytest.raises(AssertionError):
        OrderUpdateMessage.deserialize(order_update_message_serialized_1)

    order_update_message_serialized_2 = (
        f'ORDER_UPDATE 2024-07-19T00:00:00.000000+0000 1 1000'
    )
    with pytest.raises(AssertionError):
        OrderUpdateMessage.deserialize(order_update_message_serialized_2)
