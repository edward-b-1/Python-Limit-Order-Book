


from lib_webserver.webserver_types import FastAPI_Ticker
from lib_webserver.webserver_types import FastAPI_TopOfBook
from lib_webserver.webserver_types import FastAPI_Order
from lib_webserver.webserver_types import FastAPI_Trade

from lib_webserver.webserver_types import FastAPI_ReturnStatus
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithPing
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithOrder
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTradesAndOrderId
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTrades
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTopOfBook
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTickerList
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithOrderBoard

from lib_webserver.webserver_types import FastAPI_OrderInsertMessage
from lib_webserver.webserver_types import FastAPI_OrderUpdateMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelPartialMessage
from lib_webserver.webserver_types import FastAPI_TopOfBookMessage

from lib_datetime import datetime_to_order_board_display_string
from lib_datetime import datetime_to_string

from datetime import datetime
from datetime import timezone

from typeguard import typechecked


# import random

# random.seed(1234)

# def randomPrice():
#     return 1000 + random.randint(-50, 50)

# def randomVolume():
#     return random.randint(0, 100)


@ typechecked
class FakeWebserverImpl():

    def __init__(self) -> None:
        self._timestamp = datetime(
            year=2024, month=7, day=25,
            hour=9, minute=0, second=0,
            tzinfo=timezone.utc,
        )
        # TODO: use
        #
        # from fastapi import Depends
        # def now() -> datetime:
        #     now_impl = Depends(get_now_function)
        #     return now_impl()
        #
        # ? (put this code outside this class)

    def close(self) -> None:
        pass


    def get_datetime(self) -> datetime:
        return self._timestamp


    def set_datetime(self, timestamp:datetime) -> None:
        self._timestamp = timestamp


    def send_order(
        self,
        fastapi_order_insert_message: FastAPI_OrderInsertMessage,
    ) -> FastAPI_ReturnStatusWithTradesAndOrderId:
        order_id = 2
        trade = FastAPI_Trade(
            trade_id=1,
            timestamp=datetime_to_string(self._timestamp),
            order_id_maker=1,
            order_id_taker=2,
            ticker='EXAMPLE_TICKER',
            price=1000,
            volume=10,
        )
        trades = [trade]
        return FastAPI_ReturnStatusWithTradesAndOrderId(
            status='success',
            message='no message',
            order_id=order_id,
            trades=trades,
        )


    def update_order(
        self,
        fastapi_order_update_message: FastAPI_OrderUpdateMessage,
    ) -> FastAPI_ReturnStatusWithTrades:

        trade = FastAPI_Trade(
            trade_id=1,
            timestamp=datetime_to_string(self._timestamp),
            order_id_maker=1,
            order_id_taker=2,
            ticker='EXAMPLE_TICKER',
            price=1000,
            volume=10,
        )
        trades = [trade]
        return FastAPI_ReturnStatusWithTrades(
            status='success',
            message='no message',
            trades=trades,
        )

    def cancel_order_partial(
        self,
        fastapi_order_cancel_partial_message: FastAPI_OrderCancelPartialMessage,
    ) -> FastAPI_ReturnStatus:

        return FastAPI_ReturnStatus(
            status='success',
            message='no message',
        )


    def cancel_order(
        self,
        fastapi_order_cancel_message: FastAPI_OrderCancelMessage,
    ) -> FastAPI_ReturnStatus|FastAPI_ReturnStatusWithOrder:

        order = FastAPI_Order(
            order_id=1,
            timestamp=datetime_to_string(self._timestamp),
            order_side='BUY',
            price=1000,
            ticker='EXAMPLE_TICKER',
            volume=10,
        )
        return FastAPI_ReturnStatusWithOrder(
            status='success',
            message='no message',
            order=order,
        )


    def top_of_book(
        self,
        fastapi_ticker: FastAPI_TopOfBookMessage,
    ) -> FastAPI_ReturnStatusWithTopOfBook:

        fastapi_top_of_book = FastAPI_TopOfBook(
            ticker=fastapi_ticker.ticker,
            price_buy=1000,
            volume_buy=100,
            price_sell=990,
            volume_sell=50,
        )
        r = FastAPI_ReturnStatusWithTopOfBook(
            status='success',
            message='no message',
            top_of_book=fastapi_top_of_book,
        )
        return r


    def list_all_tickers(
        self,
    ) -> FastAPI_ReturnStatusWithTickerList:

        tickers = ['EXAMPLE_TICKER']
        return FastAPI_ReturnStatusWithTickerList(
            status='success',
            message='no message',
            tickers=tickers,
        )


    def order_board(self) -> FastAPI_ReturnStatusWithOrderBoard:

        order = FastAPI_Order(
            order_id=1,
            timestamp=datetime_to_order_board_display_string(self._timestamp),
            ticker='EXAMPLE_TICKER',
            order_side='BUY',
            price=1000,
            volume=10,
        )
        orders = [order]
        return FastAPI_ReturnStatusWithOrderBoard(
            status='success',
            message='no message',
            orders=orders,
        )


    def trades(self) -> FastAPI_ReturnStatusWithTrades:

        trade = FastAPI_Trade(
            trade_id=1,
            timestamp=datetime_to_string(self._timestamp),
            order_id_maker=1,
            order_id_taker=2,
            ticker='EXAMPLE_TICKER',
            price=1000,
            volume=10,
        )
        trades = [trade]
        return FastAPI_ReturnStatusWithTrades(
            status='success',
            message='no message',
            trades=trades,
        )


    def ping(self) -> FastAPI_ReturnStatusWithPing:
        return FastAPI_ReturnStatusWithPing(
            status='success',
            message='no message',
            ping='pong',
        )


    def debug_log_top_of_book(self, fastapi_ticker: FastAPI_Ticker) -> FastAPI_ReturnStatus:
        return FastAPI_ReturnStatus(
            status='success',
            message='no message',
        )


    def debug_log_current_order_id(self) -> FastAPI_ReturnStatus:
        return FastAPI_ReturnStatus(
            status='success',
            message='no message',
        )


    def debug_log_all_tickers(self) -> FastAPI_ReturnStatus:
        return FastAPI_ReturnStatus(
            status='success',
            message='no message',
        )

