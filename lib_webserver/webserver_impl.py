
from lib_webserver.webserver_types import FastAPI_Order
from lib_webserver.webserver_types import FastAPI_Ticker

from lib_webserver.webserver_types import FastAPI_OrderInsertMessage
from lib_webserver.webserver_types import FastAPI_OrderUpdateMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelPartialMessage

from lib_webserver.webserver_types import FastAPI_TopOfBookMessage

from lib_webserver.webserver_types import FastAPI_ReturnStatus
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithPing
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithOrder
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTrades
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTradesAndOrderId
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTopOfBook
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTickerList
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithOrderBoard

from lib_financial_exchange.financial_exchange_types import Ticker

from lib_webserver.limit_order_book_event_log_adapter import LimitOrderBookEventLogAdapter
from lib_financial_exchange import TradeRecordBook

from lib_webserver.convert_fastapi_message_to_internal_message import convert_fastapi_message_to_internal_message

from lib_webserver.convert_trades_to_fastapi_trades import convert_trades_to_fastapi_trades
from lib_webserver.convert_ticker_list_to_fastapi_ticker_list import convert_ticker_list_to_fastapi_ticker_list
from lib_webserver.convert_top_of_book_to_fastapi_top_of_book import convert_top_of_book_to_fastapi_top_of_book
from lib_webserver.convert_order_to_fastapi_order import convert_order_to_fastapi_order
from lib_webserver.convert_order_list_to_fastapi_order_list import convert_order_list_to_fastapi_order_list

from lib_webserver.webserver_logging import log

from typeguard import typechecked

from lib_datetime import now


@typechecked
class WebserverImpl():

    # TODO: having all these flags is garbage
    # there should be at least 3 types:
    # WebserverImpl (normal implementation)
    # WebserverFakeDatetimeImpl (normal business logic, fake datetime object
    # which can be controlled from within a test environment)
    # WebserverFake (fake implementation of business logic, close to NOOP in
    # most cases, plus fake datetime object which can be controlled within a
    # test environment)
    #
    # The first of these is for normal production running mode and UAT testing
    # The second of these is for end-to-end unit tests, which need to control
    # the simulated datetime, but require the business logic implementation to
    # be the same
    # The final of these is for simple tests which test the FastAPI paths,
    # serialization and deserialization of data types
    #
    def __init__(
        self,
        event_log_disabled: bool = False,
    ) -> None:

        trades = []
        self._limit_order_book = LimitOrderBookEventLogAdapter(
            returned_trade_list=trades,
            event_log_file_path_override=None,
            event_log_disabled=event_log_disabled,
        )

        self._trade_record_book = TradeRecordBook()
        # TODO: add an OrderBoard data structure which follows the lifecycle of each order by order id
        # will need a new, slightly different order, which records the original order volume, how much
        # has been cancelled, how much has been filled, how much remains "open out" (in the market)
        self._trade_record_book.add_trades(trades)


    def close(self) -> None:
        self._limit_order_book.close()


    def send_order(
        self,
        fastapi_order_insert_message: FastAPI_OrderInsertMessage,
    ) -> FastAPI_ReturnStatusWithTradesAndOrderId:

        order_insert_message = convert_fastapi_message_to_internal_message(fastapi_order_insert_message, timestamp=now())
        (order_id, trades) = self._limit_order_book.order_insert(order_insert_message)

        self._trade_record_book.add_trades(trades)

        fastapi_trades = convert_trades_to_fastapi_trades(trades)
        return FastAPI_ReturnStatusWithTradesAndOrderId(
            status='success',
            message=None,
            order_id=order_id.to_int(),
            trades=fastapi_trades
        )


    def update_order(
        self,
        fastapi_order_update_message: FastAPI_OrderUpdateMessage,
    ) -> FastAPI_ReturnStatusWithTrades:

        order_update_message = convert_fastapi_message_to_internal_message(fastapi_order_update_message, timestamp=now())
        trades = self._limit_order_book.order_update(order_update_message)

        self._trade_record_book.add_trades(trades)

        fastapi_trades = convert_trades_to_fastapi_trades(trades)
        return FastAPI_ReturnStatusWithTrades(
            status='success',
            message=None,
            trades=fastapi_trades,
        )


    def cancel_order_partial(
        self,
        fastapi_order_cancel_partial_message: FastAPI_OrderCancelPartialMessage,
    ) -> FastAPI_ReturnStatus:

        order_cancel_partial_message = convert_fastapi_message_to_internal_message(fastapi_order_cancel_partial_message, timestamp=now())
        self._limit_order_book.order_cancel_partial(order_cancel_partial_message)

        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )


    def cancel_order(
        self,
        fastapi_order_cancel_message: FastAPI_OrderCancelMessage,
    ) -> FastAPI_ReturnStatus|FastAPI_ReturnStatusWithOrder:

        order_cancel_message = convert_fastapi_message_to_internal_message(fastapi_order_cancel_message, timestamp=now())
        order = self._limit_order_book.order_cancel(order_cancel_message)

        if order is None:
            return FastAPI_ReturnStatus(
                status='success',
                message=f'order id {fastapi_order_cancel_message.order_id} does not exist, no order to cancel',
            )
        else:
            fastapi_order = convert_order_to_fastapi_order(order)
            return FastAPI_ReturnStatusWithOrder(
                status='success',
                message=f'order id {fastapi_order_cancel_message.order_id} cancelled',
                order=fastapi_order,
            )


    def top_of_book(
        self,
        fastapi_top_of_book_message: FastAPI_TopOfBookMessage,
    ) -> FastAPI_ReturnStatusWithTopOfBook:
        print(f'now=')
        print(now())

        top_of_book_message = convert_fastapi_message_to_internal_message(fastapi_top_of_book_message, timestamp=now())
        top_of_book = self._limit_order_book.top_of_book(top_of_book_message)

        fastapi_top_of_book = convert_top_of_book_to_fastapi_top_of_book(top_of_book)
        r = FastAPI_ReturnStatusWithTopOfBook(
            status='success',
            message=None,
            top_of_book=fastapi_top_of_book,
        )
        return r


    def list_all_tickers(
        self,
    ) -> FastAPI_ReturnStatusWithTickerList:
        ticker_list = self._limit_order_book.list_all_tickers()
        ticker_list_str = convert_ticker_list_to_fastapi_ticker_list(ticker_list)
        return FastAPI_ReturnStatusWithTickerList(
            status='success',
            message=None,
            tickers=ticker_list_str,
        )


    def order_board(
        self,
    ) -> FastAPI_ReturnStatusWithOrderBoard:
        orders = self._limit_order_book.order_board()
        fastapi_orders = convert_order_list_to_fastapi_order_list(orders)
        return FastAPI_ReturnStatusWithOrderBoard(
            status='success',
            message=None,
            orders=fastapi_orders
        )


    def trades(
        self,
    ) -> FastAPI_ReturnStatusWithTrades:
        trade_list = self._trade_record_book.get_trades()

        fastapi_trades = convert_trades_to_fastapi_trades(trade_list)
        return FastAPI_ReturnStatusWithTrades(
            status='success',
            message=None,
            trades=fastapi_trades,
        )


    def ping(
        self,
    ) -> FastAPI_ReturnStatusWithPing:
        return FastAPI_ReturnStatusWithPing(
            status='success',
            message=None,
            ping='pong',
        )


    def debug_log_top_of_book(
        self,
        fastapi_ticker: FastAPI_Ticker,
    ) -> FastAPI_ReturnStatus:
        ticker = Ticker(ticker=fastapi_ticker.ticker)
        top_of_book = self._limit_order_book.top_of_book(ticker=ticker)
        log.debug(top_of_book)
        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )


    def debug_log_current_order_id(
        self,
    ) -> FastAPI_ReturnStatus:
        order_id = self._limit_order_book.debug_current_order_id()
        log.debug(order_id)
        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )


    def debug_log_all_tickers(
        self,
    ) -> FastAPI_ReturnStatus:
        tickers = self._limit_order_book.list_all_tickers()
        tickers_str = (
            ' '
            .join(
                map(
                    lambda ticker: ticker.to_str(),
                    tickers,
                )
            )
        )
        log.debug(f'all tickers: {tickers_str}')
        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )

