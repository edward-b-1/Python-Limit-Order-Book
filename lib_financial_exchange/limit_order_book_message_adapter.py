
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import TopOfBook

from lib_financial_exchange.financial_exchange_types.message_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderUpdateMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelPartialMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelMessage

from lib_financial_exchange.financial_exchange_types.message_types import TopOfBookMessage

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

    def order_insert(self, order_insert_message: OrderInsertMessage) -> tuple[OrderId, list[Trade]]:

        ticker = order_insert_message.to_ticker()
        order_side = order_insert_message.to_order_side()
        int_price = order_insert_message.to_int_price()
        volume = order_insert_message.to_volume()
        timestamp = order_insert_message.to_timestamp()

        return self._limit_order_book.order_insert(
            ticker=ticker,
            order_side=order_side,
            int_price=int_price,
            volume=volume,
            timestamp=timestamp,
        )

    def order_update(self, order_update_message: OrderUpdateMessage) -> list[Trade]:

        order_id = order_update_message.to_order_id()
        int_price = order_update_message.to_int_price()
        volume = order_update_message.to_volume()
        timestamp = order_update_message.to_timestamp()

        return self._limit_order_book.order_update(
            order_id=order_id,
            int_price=int_price,
            volume=volume,
            timestamp=timestamp,
        )

    def order_cancel_partial(self, order_cancel_partial_message: OrderCancelPartialMessage) -> None:

        order_id = order_cancel_partial_message.to_order_id()
        volume = order_cancel_partial_message.to_volume()

        return self._limit_order_book.order_cancel_partial(
            order_id=order_id,
            volume=volume,
        )

    def order_cancel(self, order_cancel_message: OrderCancelMessage) -> Order|None:

        order_id = order_cancel_message.to_order_id()

        return self._limit_order_book.order_cancel(
            order_id=order_id,
        )

    def top_of_book(self, top_of_book_message: TopOfBookMessage) -> TopOfBook:
        ticker = top_of_book_message.to_ticker()
        return self._limit_order_book.top_of_book(ticker)

    def list_all_tickers(self) -> list[Ticker]:
        return self._limit_order_book.list_all_tickers()

    # Should the LOB retain the information about trades?
    # def trades(self) -> list[Trade]:
    #     return self._limit_order_book.trades()

    def debug_current_order_id(self) -> OrderId:
        return self._limit_order_book.debug_current_order_id()

