
from lib_webserver.webserver_types import FastAPI_OrderInsertMessage
from lib_webserver.webserver_types import FastAPI_OrderUpdateMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelPartialMessage
from lib_webserver.webserver_types import FastAPI_TopOfBookMessage

from lib_webserver.webserver_types import FastAPI_Ticker
from lib_webserver.webserver_types import FastAPI_OrderInsertMessage

from lib_webserver.webserver_types import FastAPI_ReturnStatus
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithPing
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTrades
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTopOfBook
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTickerList
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithOrderBoard

from lib_webserver.webserver_impl import WebserverImplReal
from lib_webserver.webserver_impl import WebserverImplRealWithFakeDatetimeProxy
from lib_webserver.webserver_fake_impl import FakeWebserverImpl

from typeguard import typechecked

from enum import StrEnum

class WebserverImplementationMode(StrEnum):
    # The default (real) webserver implementation
    DEFAULT = 'DEFAULT'
    # The default (real) webserver implementation, but with a fake (test) datetime proxy
    WITH_FAKE_DATETIME_PROXY = 'WITH_FAKE_DATETIME_PROXY'
    # The fake (test) webserver implementation, the datetime proxy is also fake
    TEST = 'TEST'


@typechecked
class Webserver():

    def __init__(
        self,
        webserver_implementation_mode: WebserverImplementationMode = WebserverImplementationMode.DEFAULT,
        event_log_disabled: bool = False,
    ) -> None:
        if webserver_implementation_mode == WebserverImplementationMode.TEST:
            self._webserver = FakeWebserverImpl()
        elif webserver_implementation_mode == WebserverImplementationMode.WITH_FAKE_DATETIME_PROXY:
            self._webserver = WebserverImplRealWithFakeDatetimeProxy(
                event_log_disabled=event_log_disabled,
            )
        else: # TODO: else here or elif with a raise
            self._webserver = WebserverImplReal(
                event_log_disabled=event_log_disabled,
            )

    def close(self) -> None:
        self._webserver.close()

    def send_order(self, fastapi_order_insert_message: FastAPI_OrderInsertMessage):
        return self._webserver.send_order(fastapi_order_insert_message)

    def update_order(self, fastapi_order_update_message: FastAPI_OrderUpdateMessage):
        return self._webserver.update_order(fastapi_order_update_message)

    def cancel_order_partial(self, fastapi_order_cancel_partial_message: FastAPI_OrderCancelPartialMessage):
        return self._webserver.cancel_order_partial(fastapi_order_cancel_partial_message)

    def cancel_order(self, fastapi_order_cancel_message: FastAPI_OrderCancelMessage):
        return self._webserver.cancel_order(fastapi_order_cancel_message)

    def top_of_book(self, fastapi_top_of_book_message: FastAPI_TopOfBookMessage) -> FastAPI_ReturnStatusWithTopOfBook:
        return self._webserver.top_of_book(fastapi_top_of_book_message)

    def list_all_tickers(self) -> FastAPI_ReturnStatusWithTickerList:
        return self._webserver.list_all_tickers()

    def order_board(self) -> FastAPI_ReturnStatusWithOrderBoard:
        return self._webserver.order_board()

    def trades(self) -> FastAPI_ReturnStatusWithTrades:
        return self._webserver.trades()

    def ping(self) -> FastAPI_ReturnStatusWithPing:
        return self._webserver.ping()

    def debug_log_top_of_book(self, fastapi_ticker: FastAPI_Ticker) -> FastAPI_ReturnStatus:
        return self._webserver.debug_log_top_of_book(fastapi_ticker)

    def debug_log_current_order_id(self) -> FastAPI_ReturnStatus:
        return self._webserver.debug_log_current_order_id()

    def debug_log_all_tickers(self) -> FastAPI_ReturnStatus:
        return self._webserver.debug_log_all_tickers()

