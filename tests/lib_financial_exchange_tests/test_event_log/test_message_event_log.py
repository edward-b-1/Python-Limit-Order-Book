
from lib_event_log import InputMessageEventLog
from lib_event_log import OutputMessageEventLog

from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from lib_financial_exchange.financial_exchange_types import OrderInsertMessage

from datetime import datetime
from datetime import timezone

import os


def test_message_event_log():

    file_path = './message_event_log.txt'

    if os.path.exists(file_path):
        os.remove(file_path)

    timestamp = datetime(
        year=2024, month=7, day=22,
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

    messages = [order_insert_message]

    with OutputMessageEventLog(file_path) as output_event_log:
        for message in messages:
            output_event_log.write(message)

    with InputMessageEventLog(file_path) as input_event_log:
        for index, message in enumerate(input_event_log):
            expected_message = messages[index]
            assert message == expected_message, f'message {message} does not match expected message {expected_message}'

    os.remove(file_path)

