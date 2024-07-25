
from lib_event_log import InputTextEventLog
from lib_event_log import OutputTextEventLog

from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume

from lib_financial_exchange.financial_exchange_types import OrderInsertMessage

import os


def test_text_event_log():

    file_path = './text_event_log.txt'

    if os.path.exists(file_path):
        os.remove(file_path)

    message_1 = f'message_1'
    message_2 = f'message_2'
    message_3 = f'message_3'
    messages = [message_1, message_2, message_3]

    with OutputTextEventLog(file_path) as output_event_log:
        for message in messages:
            output_event_log.write(message)

    with InputTextEventLog(file_path) as input_event_log:
        for index, line in enumerate(input_event_log):
            expected_message = messages[index]
            assert line == expected_message, f'message {line} does not match expected message {expected_message}'

    os.remove(file_path)

