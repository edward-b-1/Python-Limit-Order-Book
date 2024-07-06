
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.trade import Trade
from limit_order_book.order import Order
from limit_order_book.exceptions import DuplicateOrderIdError

from limit_order_book.order_priority_queue import OrderPriorityQueue

#from functools import reduce
from more_itertools import consume

from typeguard import typechecked


@typechecked
class SingleSideLimitOrderBook():

    def __init__(
        self,
        ticker: Ticker,
        order_side: OrderSide,
    ) -> None:
        self._ticker = ticker
        self._order_side = order_side
        self._price_levels: dict[IntPrice, OrderPriorityQueue] = {}


    def number_of_orders(self) -> int:
        return (
            sum(
                map(
                    lambda order_priority_queue: order_priority_queue.number_of_orders(),
                    self._price_levels.values(),
                )
            )
        )


    def trade(self, taker_order: Order) -> list[Trade]:
        assert taker_order.to_ticker() == self._ticker, f'SingleSideLimitOrderBook.trade ticker mismatch'
        assert taker_order.to_order_side().other_side() == self._order_side, f'SingleSideLimitOrderBook.trade order side mismatch'

        # a taker order can trade at all prices up to the taker_order price
        # but it should be filled at the lowest price possible if it is a buy
        # or the highest price possible if it is a sell

        #if taker_order.to_order_side() == OrderSide.BUY:
        if self._order_side == OrderSide.SELL:
            # search price levels from lowest sell price to highest sell price
            # where sell price is less than or equal to buy price

            buy_price = taker_order.to_int_price()

            sell_price_levels = (
                list(
                    filter(
                        lambda key: key <= buy_price,
                        self._price_levels.keys(),
                    )
                )
            )

            price_levels = sorted(sell_price_levels, reverse=False) # small/low/cheap price comes first
            # lowest sell prices matched first, but matched at buy (bid) price

        #elif taker_order.to_order_side() == OrderSide.SELL:
        elif self._order_side == OrderSide.BUY:
            # search price levels from highest buy price to lowest buy price
            # where buy price is greater than or equal to sell price

            sell_price = taker_order.to_int_price()

            buy_price_levels = (
                list(
                    filter(
                        lambda key: key >= sell_price,
                        self._price_levels.keys(),
                    )
                )
            )

            price_levels = sorted(buy_price_levels, reverse=True) # large/high/expensive price comes first
            # highest buy prices matched first, but matched at sell (offer) price

        trade_list = []
        for price_level in price_levels:
            if taker_order.to_volume().is_zero():
                # nothing further to match, quit
                break

            order_priority_queue = self._price_levels[price_level]
            trades = order_priority_queue.trade(taker_order)
            if trades is not None:
                trade_list += trades
            else:
                raise RuntimeError(f'SingleSideLimitOrderBook.trade: unreachable condition')
        return trade_list

        # matchable_price_levels_iter = iter(price_levels)
        # for price_level in price_levels
        # while taker_order.to_volume().is_not_zero() and (price_level = next(matchable_price_levels_iter)):
        #     price_level = ...something...
        #     trades = price_level.trade(taker_order)
        #     if trades is not None:
        #         trade_list += trades
        #     else:
        #         ... can this happen ? is it expected to be possible?


    # expect can be used for API or Databento
    def insert(self, order: Order):
        assert order.to_ticker() == self._ticker, f'SingleSideLimitOrderBook.insert ticker mismatch'
        assert order.to_order_side() == self._order_side, f'SingleSideLimitOrderBook.insert order side mismatch'

        int_price = order.to_int_price()
        self._initialize_price_level(int_price)

        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise DuplicateOrderIdError(order_id)

        self._price_levels[int_price].insert(order)


    # API style interface
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
                        lambda order_priority_queue: order_priority_queue.update(order_id, int_price, volume),
                        self._price_levels.values(),
                    )
                )
            )
        )

        assert len(modified_orders) <= 1,  f'SingleSideLimitOrderBook.update invalid number of modified orders'
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
                        lambda order_priority_queue: order_priority_queue.update_int_price(order_id, int_price),
                        self._price_levels.values(),
                    )
                )
            )
        )

        assert len(modified_orders) <= 1,  f'SingleSideLimitOrderBook.update_int_price invalid number of modified orders'
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
                        lambda order_priority_queue: order_priority_queue.update_volume(order_id, volume),
                        self._price_levels.values(),
                    )
                )
            )
        )

        assert len(modified_orders) <= 1,  f'SingleSideLimitOrderBook.update_volume invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    # This function implementation is a bit weird:
    # 1. From the point of view of the API, want to change the order by OrderId
    #    don't really want to have to supply the redundant TICKER or ORDER_SIDE
    #    fields. So this function, for the API user, should be changed to take
    #    3 arguments: order_id, int_price, volume. One of int_price and volume
    #    should be nullable, meaning that it doesn't have to be provided. If the
    #    argument is not provided, then do not modify that value. NOTE: This
    #    should be the top level API only. This style will contain a lot of
    #    logic, so for the lower level APIs it would be better to have 3
    #    functions: `update`, `update_int_price`, `update_volume`. That makes
    #    the APIs for these lower level object hard to use wrong.
    #
    # 2. From the point of view of databento data feed, Modify presumably
    #    has a ORDER_ID, TICKER, ORDER_SIDE, PRICE, VOLUME. Where the PRICE
    #    and VOLUME indicate the new values, and TICKER, ORDER_SIDE do not
    #    change. (But this might be wrong, perhaps they can change.)
    #
    #    I don't recall seeing a Modify message in the data yet, so for now
    #    I will not implement the Databento modify function. (This is the
    #    previous implementation for `update`, it may not require changing
    #    for Databento data feed semantics.)
    # def modify_databento(self, order: Order) -> Order|None:
    #     # TODO: a better implementation of this would be to simply call
    #     # update on every price level, collect the returned orders,
    #     # feed them back to the top (?) level, call trade(), and then call
    #     # insert()
    #     # NOTE: [DONE] ?

    #     assert order.to_ticker() == self._ticker, f'SingleSideLimitOrderBook.update ticker mismatch'
    #     assert order.to_order_side() == self._order_side, f'SingleSideLimitOrderBook.update order side mismatch'

    #     price_level_changed_orders = (
    #         list(
    #             filter(
    #                 lambda order: order is not None,
    #                 map(
    #                     lambda order_priority_queue: order_priority_queue.modify_databento(order),
    #                     self._price_levels.values(),
    #                 )
    #             )
    #         )
    #     )

    #     # the above filter logic means that this is actually not possible
    #     assert len(price_level_changed_orders) <= 1, f'SingleSideLimitOrderBook.update invalid number of modified price level orders'
    #     if len(price_level_changed_orders) == 1:
    #         return price_level_changed_orders[0]
    #     return None

        # assert order.to_ticker() == self._ticker, f'SingleSideLimitOrderBook.update ticker mismatch'
        # assert order.to_order_side() == self._order_side, f'SingleSideLimitOrderBook.update order side mismatch'

        # order_id = order.to_order_id()
        # int_price = order.to_int_price()

        # # the order id should exist, but does it have the same int_price?

        # existing_int_price = self.find_order_int_price_by_order_id(order_id)
        # if existing_int_price is None:
        #     raise RuntimeError(f'cannot update order with order id {order_id}, order not found')

        # if int_price == existing_int_price:
        #     self._price_levels[existing_int_price].update(order)
        # else:
        #     existing_order = self._price_levels[existing_int_price].cancel(order)
        #     return existing_order
        #     # NOTE: I don't like that this returns the existing order rather than
        #     # completing the order updating process. The return value needs to
        #     # be tested for trades and then inserted again. The function name
        #     # doesn't match the behaviour. On the other hand, aggregating the
        #     # trade behaviour into the insert function is not good either.
        #     #
        #     # Could perhaps make it a bit more consistent by having the update
        #     # function of `OrderPriorityQueue` returning the Order if the price
        #     # level is changed.
        # return None


    def cancel(self, order_id: OrderId) -> Order|None:
        cancelled_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda price_level: price_level.cancel(order_id),
                        self._price_levels.values(),
                    )
                )
            )
        )

        assert len(cancelled_orders) <= 1, f'SingleSideLimitOrderBook.cancel invalid number of orders'
        if len(cancelled_orders) == 1:
            return cancelled_orders[0]
        return None


    def cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        consume(
            map(
                lambda price_level: price_level.cancel_partial(order_id, volume),
                self._price_levels.values(),
            )
        )


    def order_id_exists(self, order_id: OrderId) -> bool:
        matching_price_levels = (
            list(
                filter(
                    lambda order_id_exists_bool: order_id_exists_bool == True,
                    map(
                        lambda price_level: price_level.order_id_exists(order_id),
                        self._price_levels.values(),
                    )
                )
            )
        )

        assert len(matching_price_levels) <= 1, f'SingleSideLimitOrderBook.order_id_exists invalid number of matching price levels found'
        return len(matching_price_levels) == 1


    # def find_order_int_price_by_order_id(self, order_id: OrderId) -> OrderId|None:
    #     matching_price_levels = (
    #         list(
    #             map(
    #                 lambda price_level_key_value: price_level_key_value[0],
    #                 filter(
    #                     lambda price_level_key_value: price_level_key_value[1].order_id_exists(),
    #                     self._price_levels.items(),
    #                 )
    #             )
    #         )
    #     )

    #     assert len(matching_price_levels) <= 1, f'SingleSideLimitOrderBook.find_order_int_price_by_order_id invalid number of order ids found'
    #     if len(matching_price_levels) == 1:
    #         return matching_price_levels[0]
    #     return None


    # def find_order_by_order_id(self, order_id: OrderId) -> Order|None:
    #     matching_orders = (
    #         list(
    #             filter(
    #                 lambda object: object is not None,
    #                 map(
    #                     lambda price_level: price_level.find_order_by_order_id(order_id),
    #                     self._price_levels.values(),
    #                 )
    #             )
    #         )
    #     )

    #     assert len(matching_orders) <= 1, f'SingleSideLimitOrderBook.find_order_by_order_id invalid number of orders found'

    #     if len(matching_orders) == 1:
    #         return matching_orders[0]
    #     return None


    def _initialize_price_level(self, int_price: IntPrice) -> None:
        if not int_price in self._price_levels:
            self._price_levels[int_price] = (
                OrderPriorityQueue(
                    ticker=self._ticker,
                    order_side=self._order_side,
                    int_price=int_price,
                )
            )


    # def _filter_orders_matching_order_id(self, order_id: OrderId) -> list[Order]:
    #     return (
    #         reduce(
    #             list.__add__,
    #             filter(
    #                 lambda order_list: len(order_list) > 0,
    #                 map(
    #                     lambda price_level: price_level._filter_orders_matching_order_id(order_id),
    #                     self._price_levels.values(),
    #                 )
    #             ),
    #             [],
    #         )
    #     )


    def top_of_book(self) -> tuple[IntPrice|None, Volume|None]:

        def filter_non_empty_price_levels(price_level: tuple[IntPrice, OrderPriorityQueue]) -> bool:
            return price_level[1].number_of_orders() > 0

        def extract_key(price_level: tuple[IntPrice, OrderPriorityQueue]) -> IntPrice:
            return price_level[0]

        if self._order_side == OrderSide.BUY:
            if len(self._price_levels) > 0:
                max_non_zero_price_level = (
                    max(
                        filter(
                            filter_non_empty_price_levels,
                            self._price_levels.items(),
                        ),
                        default=None,
                        key=extract_key,
                    )
                )
                if max_non_zero_price_level is None:
                    return (None, None)
                #price_level = max(self._price_levels.keys())
                price_level = extract_key(max_non_zero_price_level)
                volume = self._price_levels[price_level].total_volume()
                return (price_level, volume)
            else:
                return (None, None)
        elif self._order_side == OrderSide.SELL:
            if len(self._price_levels) > 0:
                min_non_zero_price_level = (
                    min(
                        filter(
                            filter_non_empty_price_levels,
                            self._price_levels.items(),
                        ),
                        default=None,
                        key=extract_key,
                    )
                )
                if min_non_zero_price_level is None:
                    return (None, None)
                #price_level = min(self._price_levels.keys())
                price_level = extract_key(min_non_zero_price_level)
                volume = self._price_levels[price_level].total_volume()
                return (price_level, volume)
            else:
                return (None, None)

