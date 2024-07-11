

from limit_order_book.types import OrderId
from limit_order_book.types import OrderSide
from limit_order_book.order import Order
from limit_order_book.order_without_order_id import OrderWithoutOrderId
from limit_order_book.trade import Trade
from limit_order_book.types import Ticker
from limit_order_book.types import IntPrice
from limit_order_book.types import Volume
from limit_order_book.top_of_book import TopOfBook
from limit_order_book.limit_order_book_wrapper import LimitOrderBook
from limit_order_book.logging import log

from typeguard import typechecked

import atexit

from datetime import datetime
from datetime import timezone

import os

'''
Need to perform processing on the Databento data first to create a list of
messages which can be used to test the order book.
'''


def now() -> datetime:
    return datetime.now(timezone.utc)

def now_string() -> str:
    datetime_now = now()
    return datetime_to_string(datetime_now)

def datetime_to_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')


@typechecked
class LimitOrderBookLogged():

    def __init__(self) -> None:
        log.info(f'LimitOrderBookLogged start')
        self._limit_order_book = LimitOrderBook()
        self._log_filename = '/python-limit-order-book-data/limit_order_book_log_file.txt'
        self._log_file = None
        atexit.register(self._cleanup)
        self._initialize()

    def _reset(self):
        self._limit_order_book = LimitOrderBook()

    def _initialize(self):
        if not os.path.exists(self._log_filename):
            log.error(f'{self._log_filename} does not exist')
            raise RuntimeError(f'path {self._log_filename} does not exist')
        else:
            if not os.path.isfile(self._log_filename):
                log.error(f'{self._log_filename} is not a file')
                raise RuntimeError(f'path {self._log_filename} exists, but is not a file')

            log_file = open(self._log_filename, 'r')
            try:
                self._reprocess_log_events(log_file)
            except Exception as exception:
                log.error(f'log file is not readable!')
                log.error(f'{exception}')
                raise
            log.info(f'initialization complete')
            log_file.close()

        log.info(f'session start')
        self._log_file = open(self._log_filename, 'a')
        datetime_now_string = now_string()
        self._log_file.write(
            f'SESSION_START {datetime_now_string}\n'
        )
        self._log_file.flush()

    def _cleanup(self):
        log.info(f'cleanup')
        datetime_now_string = now_string()
        log.info(f'session end')
        self._log_file.write(
            f'SESSION_END {datetime_now_string}\n'
        )
        self._log_file.flush()
        self._log_file.close()
        log.info(f'cleanup finished')

    def __enter__(self):
        self._initialize()
        return self

    def __exit__(self):
        self._cleanup()

    def _reprocess_log_events(self, log_file):
        log.info(f'reloading history from log file')
        for line in log_file:
            components = line.split(' ')
            assert len(components) > 0
            components_string = ', '.join(components)
            log.info(f'{len(components)}: {components_string}') # TODO: change to debug
            instruction = components[0]

            if instruction == 'ORDER_ADD':
                assert len(components) == 7, f'number of components is {len(components)}, expected 7'
                ticker_str = components[3]
                order_side_str = components[4]
                int_price_str = components[5]
                volume_str = components[6]
                order = OrderWithoutOrderId(
                    ticker=Ticker(ticker_str),
                    order_side=OrderSide(order_side_str),
                    int_price=IntPrice(int(int_price_str)),
                    volume=Volume(int(volume_str)),
                )
                self._order_insert(order=order)

            elif instruction == 'ORDER_UPDATE':
                assert len(components) == 6, f'number of components is {len(components)}, expected 6'
                order_id_str = components[3]
                int_price_str = components[4]
                volume_str = components[5]
                order_id = OrderId(int(order_id_str))
                int_price = IntPrice(int(int_price_str))
                volume = Volume(int(volume_str))
                self._order_update(order_id=order_id, int_price=int_price, volume=volume)

            elif instruction == 'ORDER_CANCEL':
                assert len(components) == 4, f'number of components is {len(components)}, expected 4'
                order_id_str = components[3]
                order_id = OrderId(int(order_id_str))
                self._order_cancel(order_id=order_id)

            elif instruction == 'ORDER_CANCEL_PARTIAL':
                assert len(components) == 5, f'number of components is {len(components)}, expected 5'
                order_id_str = components[3]
                volume_str = components[4]
                order_id = OrderId(int(order_id_str))
                volume = Volume(int(volume_str))
                self._order_cancel_partial(order_id=order_id, volume=volume)

            elif instruction == 'SESSION_START':
                pass

            elif instruction == 'SESSION_END':
                pass

            elif instruction == 'RESET':
                self._reset()

            else:
                raise RuntimeError(f'instruction {instruction} not recognized')


    def _log_order_insert(self, ip: str, order: OrderWithoutOrderId):
        ticker = order.to_ticker().to_str()
        order_side = str(order.to_order_side())
        int_price = order.to_int_price().to_int()
        volume = order.to_volume().to_int()
        datetime_now_string = now_string()
        self._log_file.write(
            f'ORDER_ADD {ip} {datetime_now_string} {ticker} {order_side} {int_price} {volume}\n'
        )
        self._log_file.flush()

    def _log_order_update(self, ip: str, order_id: OrderId, int_price: IntPrice|None, volume: Volume|None):
        order_id_int = order_id.to_int()
        int_price_int = int_price.to_int()
        volume_int = volume.to_int()
        datetime_now_string = now_string()
        self._log_file.write(
            f'ORDER_UPDATE {ip} {datetime_now_string} {order_id_int} {int_price_int} {volume_int}\n'
        )
        self._log_file.flush()

    def _log_order_cancel(self, ip: str, order_id: OrderId):
        order_id_int = order_id.to_int()
        datetime_now_string = now_string()
        self._log_file.write(
            f'ORDER_CANCEL {ip} {datetime_now_string} {order_id_int}\n'
        )
        self._log_file.flush()

    def _log_order_cancel_partial(self, ip: str, order_id: OrderId, volume: Volume):
        order_id_int = order_id.to_int()
        volume_int = volume.to_int()
        datetime_now_string = now_string()
        self._log_file.write(
            f'ORDER_CANCEL_PARTIAL {ip} {datetime_now_string} {order_id_int} {volume_int}\n'
        )
        self._log_file.flush()

    def _order_insert(self, order: OrderWithoutOrderId) -> tuple[OrderId, list[Trade]]:
        return self._limit_order_book.order_insert(order)

    def _order_update(self, order_id: OrderId, int_price: IntPrice|None, volume: Volume|None) -> list[Trade]:
        return self._limit_order_book.order_update(order_id=order_id, int_price=int_price, volume=volume)

    def _order_cancel(self, order_id: OrderId) -> Order|None:
        return self._limit_order_book.order_cancel(order_id=order_id)

    def _order_cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        return self._limit_order_book.order_cancel_partial(order_id=order_id, volume=volume)


    def order_insert(self, ip: str, order: OrderWithoutOrderId) -> tuple[OrderId, list[Trade]]:
        try:
            return_value = self._order_insert(order=order)
        finally:
            self._log_order_insert(ip=ip, order=order)
        return return_value

    def order_update(self, ip: str, order_id: OrderId, int_price: IntPrice|None, volume: Volume|None) -> list[Trade]:
        try:
            return_value = self._order_update(order_id=order_id, int_price=int_price, volume=volume)
        finally:
            self._log_order_update(ip=ip, order_id=order_id, int_price=int_price, volume=volume)
        return return_value

    def order_cancel(self, ip: str, order_id: OrderId) -> Order|None:
        try:
            return_value = self._order_cancel(order_id=order_id)
        finally:
            self._log_order_cancel(ip=ip, order_id=order_id)
        return return_value

    def order_cancel_partial(self, ip: str, order_id: OrderId, volume: Volume) -> None:
        try:
            return_value = self._order_cancel_partial(order_id=order_id, volume=volume)
        finally:
            self._log_order_cancel_partial(ip=ip, order_id=order_id, volume=volume)
        return return_value

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
