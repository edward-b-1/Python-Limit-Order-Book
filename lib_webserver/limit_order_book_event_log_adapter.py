
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import TopOfBook

from lib_financial_exchange import LimitOrderBookMessageAdapter

from lib_event_log import InputMessageEventLog
from lib_event_log import OutputMessageEventLog

from lib_financial_exchange.financial_exchange_types.message_types import AbstractMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderUpdateMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelPartialMessage
from lib_financial_exchange.financial_exchange_types.message_types import OrderCancelMessage

from lib_financial_exchange.financial_exchange_types.message_types import TopOfBookMessage

from lib_financial_exchange.financial_exchange_types.message_types import SessionStartMessage
from lib_financial_exchange.financial_exchange_types.message_types import SessionEndMessage
from lib_financial_exchange.financial_exchange_types.message_types import ResetMessage

from lib_datetime import now

import os


class LimitOrderBookEventLogAdapter():

    def __init__(self, returned_trade_list:list[Trade]=[], event_log_file_path_override:str|None=None) -> None:
        self._limit_order_book_message_adapter = LimitOrderBookMessageAdapter()
        self._event_log = None

        event_log_file_path = f'/python-limit-order-book-data/python_limit_order_book_event_log.txt'
        if event_log_file_path_override is not None:
            event_log_file_path = event_log_file_path_override

        if not os.path.exists(event_log_file_path):
            with open(event_log_file_path, 'w') as _:
                pass

        trades = []

        with InputMessageEventLog(file_path=event_log_file_path) as event_log:
            for message in event_log:
                returned_data = self._handle_message(message)
                if isinstance(returned_data, tuple):
                    # TODO: this is extremely fragile code - if return values
                    # change then this will break. add a typed structure
                    # to hold trades returned from _handle_message ?
                    returned_trades = returned_data[1]
                    trades += returned_trades
                elif isinstance(returned_data, list):
                    trades += returned_data
                else:
                    # no other return type contains trades
                    pass

        # TODO: API might be better if like `with open_input_message_event_log(filepath) as ifile:`
        event_log = OutputMessageEventLog(file_path=event_log_file_path)
        event_log.open()
        self._event_log = event_log
        self._event_log.write(
            message=SessionStartMessage(
                created_datetime=now(),
            )
        )
        returned_trade_list.clear()
        returned_trade_list += trades


    # TODO: add RAII functions, `open` function
    def close(self):
        self._event_log.write(
            message=SessionEndMessage(
                created_datetime=now(),
            )
        )
        self._event_log.close()


    # TODO: missing start, end and reset messages
    def _handle_message(self, message: AbstractMessage):
        if isinstance(message, OrderInsertMessage):
            return self._order_insert(message)
        elif isinstance(message, OrderUpdateMessage):
            return self._order_update(message)
        elif isinstance(message, OrderCancelPartialMessage):
            return self._order_cancel_partial(message)
        elif isinstance(message, OrderCancelMessage):
            return self._order_cancel(message)
        elif isinstance(message, TopOfBookMessage):
            return self._top_of_book(message)
        elif isinstance(message, SessionStartMessage):
            pass
        elif isinstance(message, SessionEndMessage):
            pass
        elif isinstance(message, ResetMessage):
            pass
            # TODO: reset logic not implemented yet
        else:
            raise TypeError(f'message type {type(message)} not valid')


    def order_insert(
        self,
        order_insert_message: OrderInsertMessage,
    ) -> tuple[OrderId, list[Trade]]:

        (order_id, trades) = self._order_insert(order_insert_message)
        self._event_log.write(message=order_insert_message)
        return (order_id, trades)


    def _order_insert(
        self,
        order_insert_message: OrderInsertMessage,
    ) -> tuple[OrderId, list[Trade]]:

        (order_id, trades) = self._limit_order_book_message_adapter.order_insert(order_insert_message)
        return (order_id, trades)


    def order_update(
        self,
        order_update_message: OrderUpdateMessage,
    ) -> list[Trade]:

        trades = self._order_update(order_update_message)
        self._event_log.write(message=order_update_message)
        return trades


    def _order_update(
        self,
        order_update_message: OrderUpdateMessage,
    ) -> list[Trade]:

        trades = self._limit_order_book_message_adapter.order_update(order_update_message)
        return trades


    def order_cancel_partial(
        self,
        order_cancel_partial_message: OrderCancelPartialMessage,
    ) -> None:

        self._order_cancel_partial(order_cancel_partial_message)
        self._event_log.write(message=order_cancel_partial_message)
        return None


    def _order_cancel_partial(
        self,
        order_cancel_partial_message: OrderCancelPartialMessage,
    ) -> None:

        self._limit_order_book_message_adapter.order_cancel_partial(order_cancel_partial_message)
        return None


    def order_cancel(
        self,
        order_cancel_message: OrderCancelMessage,
    ) -> Order|None:

        order = self._order_cancel(order_cancel_message)
        self._event_log.write(message=order_cancel_message)
        return order


    def _order_cancel(
        self,
        order_cancel_message: OrderCancelMessage,
    ) -> Order|None:

        order = self._limit_order_book_message_adapter.order_cancel(order_cancel_message)
        return order


    def top_of_book(
        self,
        top_of_book_message: TopOfBookMessage,
    ) -> TopOfBook:

        top_of_book = self._top_of_book(top_of_book_message)
        #self._event_log.write(message=top_of_book_message) # NOTE: currently don't save this event because not state changing
        return top_of_book


    def _top_of_book(
        self,
        top_of_book_message: TopOfBookMessage,
    ) -> TopOfBook:

        top_of_book = self._limit_order_book_message_adapter.top_of_book(top_of_book_message)
        return top_of_book


    def list_all_tickers(
        self,
    ) -> list[Ticker]:
        ticker_list = self._limit_order_book_message_adapter.list_all_tickers()
        return ticker_list


    def order_board(
        self,
    ) -> list[Order]:
        orders = self._limit_order_book_message_adapter.order_board()
        return orders


    def debug_current_order_id(self) -> OrderId:
        return self._limit_order_book_message_adapter.debug_current_order_id()

