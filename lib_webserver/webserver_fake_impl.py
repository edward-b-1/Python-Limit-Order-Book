


from lib_webserver.webserver_types import FastAPI_Ticker
from lib_webserver.webserver_types import FastAPI_TopOfBook
from lib_webserver.webserver_types import FastAPI_Order

from lib_webserver.webserver_types import FastAPI_ReturnStatus
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithPing
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTrades
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTopOfBook
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithTickerList
from lib_webserver.webserver_types import FastAPI_ReturnStatusWithOrderBoard

from lib_webserver.webserver_types import FastAPI_OrderInsertMessage
from lib_webserver.webserver_types import FastAPI_OrderUpdateMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelMessage
from lib_webserver.webserver_types import FastAPI_OrderCancelPartialMessage

from lib_datetime import datetime_to_order_board_display_string

from datetime import datetime
from datetime import timezone


import random

random.seed(1234)

def randomPrice():
    return 1000 + random.randint(-50, 50)

def randomVolume():
    return random.randint(0, 100)




class FakeWebserverImpl():

    def __init__(self) -> None:
        pass

    def close(self) -> None:
        pass

    # NOTE: different return structure
    def send_order(self, fastapi_order_insert_message: FastAPI_OrderInsertMessage):
        print(f'{fastapi_order_insert_message}')
        return FastAPI_ReturnStatus(
            status='success',
            message='fake endpoint ignores this post request'
        )

    # NOTE: different return structure
    def update_order(self, fastapi_order_update_message: FastAPI_OrderUpdateMessage):
        print(f'{fastapi_order_update_message}')
        return FastAPI_ReturnStatus(
            status='success',
            message='fake endpoint ignores this post request'
        )

    # NOTE: different return structure
    def cancel_order_partial(self, fastapi_order_cancel_partial_message: FastAPI_OrderCancelPartialMessage):
        print(f'{fastapi_order_cancel_partial_message}')
        return FastAPI_ReturnStatus(
            status='success',
            message='fake endpoint ignores this post request'
        )

    # NOTE: different return structure
    def cancel_order(self, fastapi_order_cancel_message: FastAPI_OrderCancelMessage):
        print(f'{fastapi_order_cancel_message}')
        return FastAPI_ReturnStatus(
            status='success',
            message='fake endpoint ignores this post request'
        )


    def top_of_book(self, fastapi_ticker: FastAPI_Ticker) -> FastAPI_ReturnStatusWithTopOfBook:
        fastapi_top_of_book = FastAPI_TopOfBook(
            ticker=fastapi_ticker.ticker,
            price_buy=randomPrice(),
            volume_buy=randomVolume(),
            price_sell=randomPrice(),
            volume_sell=randomVolume(),
        )
        r = FastAPI_ReturnStatusWithTopOfBook(
            status='success',
            message=None,
            top_of_book=fastapi_top_of_book,
        )
        return r


    def list_all_tickers(self) -> FastAPI_ReturnStatusWithTickerList:
        tickers = ['PYTH', 'RUST', 'CPP', 'JS']
        return FastAPI_ReturnStatusWithTickerList(
            status='success',
            message=None,
            tickers=tickers,
        )


    def order_board(self) -> FastAPI_ReturnStatusWithOrderBoard:
        datetime_1 = datetime(
            year=2024, month=7, day=20,
            hour=16, minute=21, second=0,
            tzinfo=timezone.utc,
        )
        order_1 = FastAPI_Order(
            order_id=1,
            timestamp=datetime_to_order_board_display_string(datetime_1),
            ticker='PYTH',
            order_side='BUY',
            price=1000,
            volume=10,
        )
        orders = [order_1]
        return FastAPI_ReturnStatusWithOrderBoard(
            status='success',
            message=None,
            orders=orders,
        )


    def trades(self) -> FastAPI_ReturnStatusWithTrades:
        raise NotImplementedError(f'not implemented yet')


    def ping(self) -> FastAPI_ReturnStatusWithPing:
        return FastAPI_ReturnStatusWithPing(
            status='success',
            message=None,
            ping='pong',
        )


    def debug_log_top_of_book(self, fastapi_ticker: FastAPI_Ticker) -> FastAPI_ReturnStatus:
        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )


    def debug_log_current_order_id(self) -> FastAPI_ReturnStatus:
        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )


    def debug_log_all_tickers(self) -> FastAPI_ReturnStatus:
        return FastAPI_ReturnStatus(
            status='success',
            message=None,
        )

