

from limit_order_book.types.order_id import OrderId
from limit_order_book.order_side import OrderSide
from limit_order_book.order import Order
from limit_order_book.order_without_order_id import OrderWithoutOrderId
from limit_order_book.trade import Trade
from limit_order_book.ticker import Ticker
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.top_of_book import TopOfBook
from limit_order_book.limit_order_book_wrapper import LimitOrderBook
from limit_order_book.logging import log

from typeguard import typechecked

import atexit

from datetime import datetime
from datetime import timezone

'''
Need to perform processing on the Databento data first to create a list of
messages which can be used to test the order book.
'''


def now() -> datetime:
    return datetime.now(timezone.utc)


@typechecked
class LimitOrderBookLogged():

    def __init__(self) -> None:
        self._limit_order_book = LimitOrderBook()
        self._log_file = None
        atexit.register(self._cleanup)

    def _initialize(self):
        self._log_file = open('limit_order_book_log_file.txt', 'w')
        datetime_now = now()
        self._log_file.write(
            f'SESSION_START {datetime_now}'
        )
        self._log_file.flush()

    def _cleanup(self):
        datetime_now = now()
        self._log_file.write(
            f'SESSION_END {datetime_now}'
        )
        self._log_file.flush()
        self._log_file.close()

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self):
        self._cleanup()

    def _log_order_insert(self, ip: str, order: OrderWithoutOrderId):
        ticker = order.to_ticker().to_str()
        order_side = str(order.to_order_side())
        int_price = order.to_int_price().to_int()
        volume = order.to_volume().to_int()
        datetime_now = now()
        self._log_file.write(
            f'ORDER_ADD {ip} {datetime_now} {ticker} {order_side} {int_price} {volume}\n'
        )
        self._log_file.flush()

    def _log_order_update(self, ip: str, order_id: OrderId, int_price: IntPrice|None, volume: Volume|None):
        order_id = order_id.to_int()
        int_price = int_price.to_int()
        volume = volume.to_int()
        datetime_now = now()
        self._log_file.write(
            f'ORDER_UPDATE {ip} {datetime_now} {order_id} {int_price} {volume}\n'
        )
        self._log_file.flush()

    def _log_order_cancel(self, ip: str, order_id: OrderId):
        order_id = order_id.to_int()
        datetime_now = now()
        self._log_file.write(
            f'ORDER_CANCEL {ip} {datetime_now} {order_id}\n'
        )
        self._log_file.flush()

    def _log_order_cancel_partial(self, ip: str, order_id: OrderId, volume: Volume):
        order_id = order_id.to_int()
        volume = volume.to_int()
        datetime_now = now()
        self._log_file.write(
            f'ORDER_CANCEL_PARTIAL {ip} {datetime_now} {order_id} {volume}\n'
        )
        self._log_file.flush()

    def order_insert(self, ip: str, order: OrderWithoutOrderId) -> tuple[OrderId, list[Trade]]:
        self._log_order_insert(ip, order)
        return self._limit_order_book.order_insert(order)

    def order_update(self, ip: str, order_id: OrderId, int_price: IntPrice|None, volume: Volume|None) -> list[Trade]:
        self._log_order_update(ip, order_id=order_id, int_price=int_price, volume=volume)
        return self._limit_order_book.order_update(order_id=order_id, int_price=int_price, volume=volume)

    def order_cancel(self, ip: str, order_id: OrderId) -> Order|None:
        self._log_order_cancel(ip=ip, order_id=order_id)
        return self._limit_order_book.order_cancel(order_id=order_id)

    def order_cancel_partial(self, ip: str, order_id: OrderId, volume: Volume) -> None:
        self._log_order_cancel_partial(ip, order_id=order_id, volume=volume)
        return self._limit_order_book.order_cancel_partial(order_id=order_id, volume=volume)

    def top_of_book(self, ticker: Ticker) -> TopOfBook:
        return self._limit_order_book.top_of_book(ticker=ticker)

    def number_of_orders(self) -> int:
        return self._limit_order_book.number_of_orders()

    def list_all_tickers(self) -> list[Ticker]:
        return self._limit_order_book.list_all_tickers()

    def debug_log_current_order_id(self) -> None:
        return self._limit_order_book.debug_log_current_order_id()

    def debug_log_top_of_book(self, ticker: Ticker) -> None:
        return self._limit_order_book.debug_log_top_of_book()

    def debug_log_all_tickers(self) -> None:
        return self._limit_order_book.debug_log_all_tickers()
