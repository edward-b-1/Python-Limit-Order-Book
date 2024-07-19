
from lib_financial_exchange.financial_exchange_types.message_types import TopOfBookMessage

from lib_financial_exchange.financial_exchange_types import Ticker

from datetime import datetime
from datetime import timezone

import pytest


def test_top_of_book_message():

    top_of_book_message = TopOfBookMessage(
        created_datetime=datetime(year=2024, month=7, day=19, tzinfo=timezone.utc),
        ticker=Ticker('PYTH'),
    )

    top_of_book_message_serialized = (
        f'TOP_OF_BOOK 2024-07-19T00:00:00.000000+0000 PYTH'
    )

    assert str(top_of_book_message) == (
        f'TopOfBookMessage(2024-07-19 00:00:00+00:00, Ticker(PYTH))'
    )

    assert top_of_book_message.serialize() == top_of_book_message_serialized

    assert TopOfBookMessage.deserialize(top_of_book_message_serialized) == top_of_book_message


def test_top_of_book_message_deserialize_wrong_number_of_fields():

    order_cancel_message_serialized_1 = (
        f'ORDER_CANCEL 2024-07-19T00:00:00.000000+0000 1 1'
    )
    with pytest.raises(AssertionError):
        TopOfBookMessage.deserialize(order_cancel_message_serialized_1)

    order_cancel_message_serialized_2 = (
        f'ORDER_CANCEL 2024-07-19T00:00:00.000000+0000'
    )
    with pytest.raises(AssertionError):
        TopOfBookMessage.deserialize(order_cancel_message_serialized_2)
