
from lib_webserver.webserver_types import FastAPI_OrderInsertMessage
from lib_webserver.webserver_types import FastAPI_OrderUpdateMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelPartialMessage
from lib_webserver.webserver_types import FastAPI_TopOfBookMessage

from lib_financial_exchange.financial_exchange_types.message_types import AbstractMessage
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import OrderUpdateMessage
from lib_financial_exchange.financial_exchange_types import OrderCancelPartialMessage
from lib_financial_exchange.financial_exchange_types import OrderCancelMessage
from lib_financial_exchange.financial_exchange_types import TopOfBookMessage

from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderId

from datetime import datetime


FastAPI_MessageUnion = (
    FastAPI_OrderInsertMessage |
    FastAPI_OrderUpdateMessage |
    FastAPI_OrderCancelPartialMessage |
    FastAPI_OrderCancelMessage |
    FastAPI_TopOfBookMessage
)

def convert_fastapi_message_to_internal_message(
    fastapi_message: FastAPI_MessageUnion,
    timestamp: datetime,
) -> AbstractMessage:

    if isinstance(fastapi_message, FastAPI_OrderInsertMessage):
        order_insert_message = OrderInsertMessage(
            created_datetime=timestamp,
            ticker=Ticker(fastapi_message.ticker),
            order_side=OrderSide(fastapi_message.order_side),
            int_price=IntPrice(fastapi_message.price),
            volume=Volume(fastapi_message.volume),
        )
        return order_insert_message

    elif isinstance(fastapi_message, FastAPI_OrderUpdateMessage):
        order_update_message = OrderUpdateMessage(
            created_datetime=timestamp,
            order_id=OrderId(fastapi_message.order_id),
            int_price=IntPrice(fastapi_message.price),
            volume=Volume(fastapi_message.volume),
        )
        return order_update_message

    elif isinstance(fastapi_message, FastAPI_OrderCancelPartialMessage):
        order_cancel_partial_message = OrderCancelPartialMessage(
            created_datetime=timestamp,
            order_id=OrderId(fastapi_message.order_id),
            volume=Volume(fastapi_message.volume),
        )
        return order_cancel_partial_message

    elif isinstance(fastapi_message, FastAPI_OrderCancelMessage):
        order_cancel_message = OrderCancelMessage(
            created_datetime=timestamp,
            order_id=OrderId(fastapi_message.order_id),
        )
        return order_cancel_message

    elif isinstance(fastapi_message, FastAPI_TopOfBookMessage):
        top_of_book_message = TopOfBookMessage(
            created_datetime=timestamp,
            ticker=Ticker(fastapi_message.ticker),
        )
        return top_of_book_message

    else:
        # TODO: write tests for unreachable (?) else case
        raise TypeError(f'unknown message type {type(fastapi_message)}')

