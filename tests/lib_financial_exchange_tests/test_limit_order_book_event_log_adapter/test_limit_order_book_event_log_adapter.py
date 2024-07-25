
from lib_webserver.limit_order_book_event_log_adapter import LimitOrderBookEventLogAdapter

from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import TradeId
from lib_financial_exchange.financial_exchange_types import Trade

from lib_financial_exchange.financial_exchange_types import OrderInsertMessage

from datetime import datetime
from datetime import timezone

import os


def run_phase_1():
    # Phase 1: Run the Limit Order Book Event Log Adapter, create an
    # Order Insert Message

    limit_order_book = LimitOrderBookEventLogAdapter(
        event_log_file_path_override=f'test_limit_order_book_event_log.txt'
    )

    timestamp = datetime(
        year=2024, month=7, day=22,
        hour=9, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    ticker = Ticker('PYTH')
    order_side = OrderSide('BUY')
    int_price = IntPrice(1000)
    volume = Volume(10)

    order_insert_message_1 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=volume,
    )

    (order_id_1, trades) = limit_order_book.order_insert(
        order_insert_message=order_insert_message_1,
    )
    assert order_id_1 == OrderId(1)
    assert trades == []

    limit_order_book.close()


def run_phase_2():
    # Phase 2: Run the Limit Order Book Event Log Adapter, create an
    # Order Insert Message, and check the OrderId is 2, not 1

    limit_order_book = LimitOrderBookEventLogAdapter(
        event_log_file_path_override=f'test_limit_order_book_event_log.txt'
    )

    timestamp = datetime(
        year=2024, month=7, day=22,
        hour=9, minute=10, second=0,
        tzinfo=timezone.utc,
    )

    ticker = Ticker('PYTH')
    order_side = OrderSide('BUY')
    int_price = IntPrice(1005)
    volume = Volume(10)

    order_insert_message_2 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=volume,
    )

    (order_id_2, trades) = limit_order_book.order_insert(
        order_insert_message=order_insert_message_2,
    )
    assert order_id_2 == OrderId(2)
    assert trades == []

    limit_order_book.close()


def run_phase_3():
    # Phase 3: Run the Limit Order Book Event Log Adapter, create an
    # Order Insert Message, and check the OrderId is 3, not 1.
    # This order will trade all of order id 1 and part of order id 2

    limit_order_book = LimitOrderBookEventLogAdapter(
        event_log_file_path_override=f'test_limit_order_book_event_log.txt'
    )

    timestamp = datetime(
        year=2024, month=7, day=22,
        hour=9, minute=20, second=0,
        tzinfo=timezone.utc,
    )

    ticker = Ticker('PYTH')
    order_side = OrderSide('SELL')
    int_price = IntPrice(995)
    volume = Volume(12)

    order_insert_message_3 = OrderInsertMessage(
        created_datetime=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=volume,
    )

    (order_id_3, trades) = limit_order_book.order_insert(
        order_insert_message=order_insert_message_3,
    )
    assert order_id_3 == OrderId(3)
    assert trades == [
        Trade(
            trade_id=TradeId(1),
            timestamp=timestamp,
            order_id_maker=OrderId(2),
            order_id_taker=OrderId(3),
            ticker=ticker,
            int_price=IntPrice(995),
            volume=Volume(10),
        ),
        Trade(
            trade_id=TradeId(2),
            timestamp=timestamp,
            order_id_maker=OrderId(1),
            order_id_taker=OrderId(3),
            ticker=ticker,
            int_price=IntPrice(995),
            volume=Volume(2),
        ),
    ]

    limit_order_book.close()


def test_limit_order_book_event_log_adapter():

    event_log_file_path_override=f'test_limit_order_book_event_log.txt'

    if os.path.exists(event_log_file_path_override):
        if os.path.isfile(event_log_file_path_override):
            os.remove(event_log_file_path_override)

    run_phase_1()
    run_phase_2()
    run_phase_3()

    os.remove(event_log_file_path_override)

