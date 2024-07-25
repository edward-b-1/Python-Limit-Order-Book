
from lib_financial_exchange.message_factory import MessageFactory

from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from lib_financial_exchange.financial_exchange_types import OrderInsertMessage

from datetime import datetime
from datetime import timezone


def test_message_factory():

    message_factory = MessageFactory()

    timestamp = datetime(
        year=2024, month=7, day=23,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    ticker = Ticker('PYTH')
    order_side = OrderSide('BUY')
    int_price = IntPrice(1000)
    volume = Volume(10)

    order_insert_message = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=volume,
    )
    serialized_message = order_insert_message.serialize()
    message = 'ORDER_INSERT 2024-07-23T09:00:00.000000+0000 PYTH BUY 1000 10'
    assert serialized_message == message, f'message format has changed'

    created_message = message_factory.create(serialized_message=message)
    print(type(created_message))
    assert created_message == order_insert_message, f'{created_message}\n{order_insert_message}'
