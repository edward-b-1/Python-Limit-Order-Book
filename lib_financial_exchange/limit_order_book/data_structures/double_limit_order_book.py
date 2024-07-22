
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import TopOfBook

from lib_financial_exchange.trade_id_generator import TradeIdGenerator

from lib_financial_exchange.exceptions import DuplicateOrderIdError

from lib_financial_exchange.limit_order_book.data_structures.single_side_limit_order_book import SingleSideLimitOrderBook

from functools import reduce
from more_itertools import consume

from datetime import datetime

from typeguard import typechecked


@typechecked
class DoubleLimitOrderBook():

    def __init__(
        self,
        ticker: Ticker,
    ) -> None:
        self._ticker = ticker
        self._buy_side_limit_order_book = SingleSideLimitOrderBook(
            ticker=ticker,
            order_side=OrderSide.BUY,
        )
        self._sell_side_limit_order_book = SingleSideLimitOrderBook(
            ticker=ticker,
            order_side=OrderSide.SELL,
        )
        self._limit_order_book = {
            OrderSide.BUY: self._buy_side_limit_order_book,
            OrderSide.SELL: self._sell_side_limit_order_book,
        }


    def number_of_orders(self) -> int:
        return (
            sum(
                map(
                    lambda single_side_limit_order_book: single_side_limit_order_book.number_of_orders(),
                    self._limit_order_book.values(),
                )
            )
        )


    def trade(self, taker_order: Order, trade_id_generator: TradeIdGenerator, timestamp: datetime) -> list[Trade]:
        assert taker_order.to_ticker() == self._ticker, f'DoubleLimitOrderBook.trade ticker mismatch'

        order_side = taker_order.to_order_side()
        other_side_order_side = order_side.other_side()

        other_side_limit_order_book = self._limit_order_book[other_side_order_side]
        trades = other_side_limit_order_book.trade(taker_order, trade_id_generator=trade_id_generator, timestamp=timestamp)
        return trades


    def insert(self, order: Order) -> None:
        assert order.to_ticker() == self._ticker, f'DoubleLimitOrderBook.insert ticker mismatch'

        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise DuplicateOrderIdError(order_id)

        order_side = order.to_order_side()

        self._limit_order_book[order_side].insert(order)
        return None


    def update(self, order_id: OrderId, int_price: IntPrice, volume: Volume) -> Order|None:
        '''
        Note: If the int_price and volume match the existing order int_price
              and volume, then this function must return None. The priority
              must not be changed if the values remain the same. This would
              be surprising to a user of the API.
        '''

        modified_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda single_side_limit_order_book: single_side_limit_order_book.update(order_id, int_price, volume),
                        self._limit_order_book.values(),
                    )
                )
            )
        )

        assert len(modified_orders) <= 1, f'DoubleLimitOrderBook.update invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    def update_int_price(self, order_id: OrderId, int_price: IntPrice) -> Order|None:
        '''
        Note: If the int_price and volume match the existing order int_price
              and volume, then this function must return None. The priority
              must not be changed if the values remain the same. This would
              be surprising to a user of the API.
        '''

        modified_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda single_side_limit_order_book: single_side_limit_order_book.update_int_price(order_id, int_price),
                        self._limit_order_book.values(),
                    )
                )
            )
        )

        assert len(modified_orders) <= 1, f'DoubleLimitOrderBook.update_int_price invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    def update_volume(self, order_id: OrderId, volume: Volume) -> Order|None:
        '''
        Note: If the int_price and volume match the existing order int_price
              and volume, then this function must return None. The priority
              must not be changed if the values remain the same. This would
              be surprising to a user of the API.
        '''

        modified_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda single_side_limit_order_book: single_side_limit_order_book.update_volume(order_id, volume),
                        self._limit_order_book.values(),
                    )
                )
            )
        )

        assert len(modified_orders) <= 1, f'DoubleLimitOrderBook.update_volume invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    def cancel(self, order_id: OrderId) -> Order|None:
        cancelled_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda single_side_limit_order_book: single_side_limit_order_book.cancel(order_id),
                        self._limit_order_book.values(),
                    )
                )
            )
        )

        assert len(cancelled_orders) <= 1, f'DoubleLimitOrderBook.cancel invalid number of orders'
        if len(cancelled_orders) == 1:
            return cancelled_orders[0]
        return None


    def cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        consume(
            map(
                lambda limit_order_book: limit_order_book.cancel_partial(order_id, volume),
                self._limit_order_book.values(),
            )
        )


    def order_id_exists(self, order_id: OrderId) -> bool:
        matching_order_sides = (
            list(
                filter(
                    lambda order_id_exists_bool: order_id_exists_bool == True,
                    map(
                        lambda single_side_limit_order_book: single_side_limit_order_book.order_id_exists(order_id),
                        self._limit_order_book.values(),
                    )
                )
            )
        )

        assert len(matching_order_sides) <= 1, f'DoubleLimitOrderBook.order_id_exists invalid number of matching order sides'
        return len(matching_order_sides) == 1


    def top_of_book(self) -> TopOfBook:

        (int_price_buy, volume_buy) = self._buy_side_limit_order_book.top_of_book()
        (int_price_sell, volume_sell) = self._sell_side_limit_order_book.top_of_book()

        top_of_book = TopOfBook(
            ticker=self._ticker,
            int_price_buy=int_price_buy,
            volume_buy=volume_buy,
            int_price_sell=int_price_sell,
            volume_sell=volume_sell,
        )
        return top_of_book


    # TODO: needs tests
    def get_all_orders(self) -> list[Order]:
        orders: list[Order] = (
            list(
                reduce(
                    list.__add__,
                    map(
                        lambda limit_order_book: limit_order_book.get_all_orders(),
                        self._limit_order_book.values(),
                    ),
                    []
                )
            )
        )
        orders.sort(key=lambda order: order.to_order_id())
        return orders

