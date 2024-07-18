

from lib_financial_exchange.financial_exchange_types.message_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderUpdateMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelPartialMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelMessage

from lib_financial_exchange.limit_order_book import LimitOrderBook


from typeguard import typechecked

'''
The purpose of this adapter class is to adapt the interface of the
LimitOrderBook, which presents an API in terms of simple types such as
`OrderId`, `IntPrice`, `Ticker`, etc, and provide an interface which instead
accepts the message types which are produced by both the REST API webserver
and the class which handles deserializing of events from the Event Log to
"Message" types.
'''


@typechecked
class LimitOrderBookMessageAdapter():

    def __init__(self) -> None:
        self._limit_order_book = LimitOrderBook()

    def order_insert(self, order_insert_message: OrderInsertMessage):

        ticker = order_insert_message.ticker
        order_side = order_insert_message.order_side
        int_price = order_insert_message.int_price
        volume = order_insert_message.volume

        self._limit_order_book.order_insert(
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
        )

    def order_update(self, order_update_message: OrderUpdateMessage):

        order_id = order_update_message.order_id
        int_price = order_update_message.int_price
        volume = order_update_message.volume

        self._limit_order_book.order_update(
            order_id=order_id,
            int_price=int_price,
            volume=volume,
        )

    def order_cancel_partial(self, order_cancel_partial_message: OrderCancelPartialMessage):

        order_id = order_cancel_partial_message.order_id
        volume = order_cancel_partial_message.volume

        self._limit_order_book.order_cancel_partial(
            order_id=order_id,
            volume=volume,
        )

    def order_cancel(self, order_cancel_message: OrderCancelMessage):

        order_id = order_cancel_message.order_id

        self._limit_order_book.order_cancel(
            order_id=order_id,
        )
