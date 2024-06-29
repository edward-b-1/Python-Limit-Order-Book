
from functools import reduce

from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.validate import *
from old_limit_order_book.order import Order
from old_limit_order_book.trade import Trade

from old_limit_order_book.limit_order_book_price_level import LimitOrderBookPriceLevel

class LimitOrderBook:

    def __init__(self, order_side: str):
        assert validate_order_side(order_side), VALIDATE_ORDER_ID_ERROR_STR
        self._order_side = order_side
        # TICKER -> PRICE_LEVEL -> list of orders and volumes
        self._limit_order_book: dict[str, LimitOrderBookPriceLevel] = {}

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        raise NotImplementedError(f'__str__ not implemented')

    def debug_str(self) -> str:
        debug_strings = []
        for ticker, price_level in self._limit_order_book.items():
            debug_strings.append(
                f'{ticker}: {price_level.debug_str()}\n'
            )
        return '\n'.join(debug_strings)

    def tickers(self) -> list[str]:
        return list(sorted(self._limit_order_book.keys()))

    def to_str(self, ticker: str) -> str:
        assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR

        if not ticker in self._limit_order_book:
            return ''

        return str(self._limit_order_book[ticker])

    def _initialize_ticker(self, ticker: str):
        if not validate_ticker(ticker):
            raise ValueError(f'ticker \'{ticker}\' is not a valid ticker')

        if not ticker in self._limit_order_book:
            self._limit_order_book[ticker] = LimitOrderBookPriceLevel(self._order_side)

    def _order_insert(self, order: Order) -> list[Trade]:
        ticker = order.to_ticker()
        return self._limit_order_book[ticker].order_insert(order)

    # Note: will actually remove all orders with order_id
    def _remove_orders_by_order_id(self, order_id: int) -> list[Order]:
        removed_orders = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda limit_order_book_price_level: limit_order_book_price_level._remove_orders_by_order_id(order_id),
                        self._limit_order_book.values(),
                    ),
                    [],
                )
            )
        )
        return removed_orders

    def _find_order_ticker_by_order_id(self, order_id: int) -> int:

        def select_ticker(key_value: tuple[int, LimitOrderBookPriceLevel]) -> int:
            return key_value[0]

        def filter_by_order_id(key_value: tuple[int, LimitOrderBookPriceLevel]) -> bool:
            limit_order_book_price_level = key_value[1]
            return limit_order_book_price_level.order_id_exists(order_id)

        tickers = (
            set(
                map(
                    select_ticker,
                    filter(
                        filter_by_order_id,
                        self._limit_order_book.items(),
                    )
                )
            )
        )

        if len(tickers) == 0:
            raise RuntimeError(f'order_id not found in limit_order_book')
        elif len(tickers) > 1:
            raise RuntimeError(f'order_id duplicated in multiple limit_order_book')

        [ticker] = tickers
        return ticker

    def _get_order_by_order_id(self, order_id: int) -> Order:
        matching_orders = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda limit_order_book_price_level: limit_order_book_price_level._filter_orders_by_order_id(order_id),
                        self._limit_order_book.values(),
                    ),
                    [],
                )
            )
        )
        assert len(matching_orders) == 1, f'_get_order_by_order_id failed'

        existing_order: Order = matching_orders[0]
        return existing_order

    def order_id_exists(self, order_id: int):
        return (
            any(
                filter(
                    lambda limit_order_book_price_level: limit_order_book_price_level.order_id_exists(order_id),
                    self._limit_order_book.values(),
                )
            )
        )

    def order_id_count(self, order_id: int) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book_price_level: limit_order_book_price_level.order_id_count(order_id),
                    self._limit_order_book.values(),
                )
            )
        )

    def depth(self, ticker: str) -> int:
        self._initialize_ticker(ticker)
        return self._limit_order_book[ticker].depth()

    def depth_aggregated(self) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book_price_level: limit_order_book_price_level.depth_aggregated(),
                    self._limit_order_book.values(),
                )
            )
        )

    def volume(self, ticker: str) -> int:
        return self._limit_order_book[ticker].volume()

    def order_insert(self, order: Order) -> list[Trade]:
        order_id = order.to_order_id()
        ticker = order.to_ticker()
        self._initialize_ticker(ticker)

        # check the order id doesn't exist
        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

        # if order_side != self.order_side:
        #     # TODO

        trade_list = self._order_insert(order)
        return trade_list
    # def order_insert(self, order_id: int, ticker: str, int_price: int, volume: int):
    #     # assert validate_ticker(ticker), VALIDATE_TICKER_ERROR_STR
    #     # assert validate_int_price(int_price), VALIDATE_INT_PRICE_ERROR_STR
    #     # assert validate_volume(volume) > 0, VALIDATE_VOLUME_ERROR_STR
    #     # ^ removed, done by Order

    #     self._initialize_ticker(ticker)

    #     # check the order id doesn't exist
    #     if self.order_id_exists(order_id):
    #         raise RuntimeError(f'cannot insert order with existing order_id {order_id}')

    #     # TODO: might make more sense to just construct this in a single place (here) and then
    #     # extract values from it rather than passing all the values down the call stack
    #     # or just duplicate them
    #     partial_order = Order().with_order_id(order_id).with_ticker(ticker).with_volume(volume)
    #     self._insert_order(partial_order)

        # TODO:
        # @static_vars(counter=0)
        # def count_order_id(order_id_volume_tuple: tuple[int, int]):
        #     assert len(order_id_volume_tuple) == 2, 'invalid order_id volume tuple'
        #     order_id_ = order_id_volume_tuple[0]
        #     if order_id_ == order_id
        #         count_order_id.counter += 1

        # consume(
        #     map(
        #         lambda price_level_order_book: consume(map(count_order_id, price_level_order_book)),
        #         ticker_order_book.values(),
        #     )
        # )

        # consume(
        #     map(
        #         count_order_id,
        #         ticker_order_book_price_level,
        #     )
        # )

        # insert the order into the lob

    def order_update(self, order_id: int, int_price: int, volume: int) -> Order|None:
        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot update order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot update order with duplicate order_id {order_id}')

        ticker = self._find_order_ticker_by_order_id(order_id)
        order = self._limit_order_book[ticker].order_update(order_id, int_price, volume)
        return order

    def order_cancel(self, order_id: int):
        # check the order id exists, and only once
        if self.order_id_count(order_id) == 0:
            raise RuntimeError(f'cannot cancel order with missing order_id {order_id}')
        elif self.order_id_count(order_id) > 1:
            raise RuntimeError(f'cannot cancel order with duplicate order_id {order_id}')

        # remove matching order
        removed_orders = self._remove_orders_by_order_id(order_id)
        assert len(removed_orders) == 1, f'unexpected number of orders removed in order_cancel'
        order: Order = removed_orders[0]
        return order
