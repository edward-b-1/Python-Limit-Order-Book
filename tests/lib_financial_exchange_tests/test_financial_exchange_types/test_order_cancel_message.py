
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelMessage

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Volume

from datetime import datetime
from datetime import timezone

import pytest


def test_order_cancel_message():

    order_cancel_message = OrderCancelMessage(
        created_datetime=datetime(year=2024, month=7, day=19, tzinfo=timezone.utc),
        order_id=OrderId(1),
    )

    order_cancel_message_serialized = (
        f'ORDER_CANCEL 2024-07-19T00:00:00.000000+0000 1'
    )

    assert str(order_cancel_message) == (
        f'OrderCancelMessage(2024-07-19 00:00:00+00:00, OrderId(1))'
    )

    assert order_cancel_message.serialize() == order_cancel_message_serialized

    assert OrderCancelMessage.deserialize(order_cancel_message_serialized) == order_cancel_message


def test_order_cancel_message_deserialize_wrong_number_of_fields():

    order_cancel_message_serialized_1 = (
        f'ORDER_CANCEL 2024-07-19T00:00:00.000000+0000 1 1'
    )
    with pytest.raises(AssertionError):
        OrderCancelMessage.deserialize(order_cancel_message_serialized_1)

    order_cancel_message_serialized_2 = (
        f'ORDER_CANCEL 2024-07-19T00:00:00.000000+0000'
    )
    with pytest.raises(AssertionError):
        OrderCancelMessage.deserialize(order_cancel_message_serialized_2)
