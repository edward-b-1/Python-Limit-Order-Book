
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

from lib_financial_exchange.financial_exchange_types import Ticker

from lib_financial_exchange import LimitOrderBookMessageAdapter

from lib_webserver.convert_fastapi_message_to_internal_message import convert_fastapi_message_to_internal_message

from lib_webserver.convert_trades_to_fastapi_trades import convert_trades_to_fastapi_trades
from lib_webserver.convert_ticker_list_to_fastapi_ticker_list import convert_ticker_list_to_fastapi_ticker_list
from lib_webserver.convert_top_of_book_to_fastapi_top_of_book import convert_top_of_book_to_fastapi_top_of_book
from lib_webserver.convert_order_to_fastapi_order import convert_order_to_fastapi_order

from lib_webserver.webserver_logging import log

from lib_datetime import now

from typeguard import typechecked


@typechecked
class WebserverImpl():

    def __init__(self) -> None:
        self._limit_order_book = LimitOrderBookMessageAdapter()

    def send_order(
        self,
        fastapi_order_insert_message: FastAPI_OrderInsertMessage,
    ) -> FastAPI_ReturnStatusWithTradesAndOrderId:

        order_insert_message = convert_fastapi_message_to_internal_message(fastapi_order_insert_message, timestamp=now())
        (order_id, trades) = self._limit_order_book.order_insert(order_insert_message)

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



    # TODO: trades stuff not implemented yet
    def trades(
        self,
    ) -> FastAPI_ReturnStatusWithTrades:
        # trade_list = trade_record.get_trades()
        trade_list = []
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

