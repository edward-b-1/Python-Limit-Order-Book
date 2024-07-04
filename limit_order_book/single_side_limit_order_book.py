
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.trade import Trade
from limit_order_book.order import Order
from limit_order_book.exceptions import DuplicateOrderIdError

from limit_order_book.order_priority_queue import OrderPriorityQueue

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


    def insert(self, order: Order):
        assert order.to_ticker() == self._ticker, f'SingleSideLimitOrderBook.insert ticker mismatch'
        assert order.to_order_side() == self._order_side, f'SingleSideLimitOrderBook.insert order side mismatch'

        int_price = order.to_int_price()
        self._initialize_price_level(int_price)

        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise DuplicateOrderIdError(order_id)

        self._price_levels[int_price].insert(order)


    def update(self, order: Order) -> Order|None:
        # TODO: a better implementation of this would be to simply call
        # update on every price level, collect the returned orders,
        # feed them back to the top (?) level, call trade(), and then call
        # insert()

        assert order.to_ticker() == self._ticker, f'SingleSideLimitOrderBook.update ticker mismatch'
        assert order.to_order_side() == self._order_side, f'SingleSideLimitOrderBook.update order side mismatch'

        price_level_changed_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda order_priority_queue: order_priority_queue.update(order),
                        self._price_levels.values(),
                    )
                )
            )
        )

        # the above filter logic means that this is actually not possible
        assert len(price_level_changed_orders) <= 1, f'SingleSideLimitOrderBook.update invalid number of modified price level orders'
        if len(price_level_changed_orders) == 1:
            return price_level_changed_orders[0]
        return None

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


    def top_of_book(self) -> tuple[IntPrice|None, Volume|None]:
        if self._order_side == OrderSide.BUY:
            if len(self._price_levels) > 0:
                price_level = max(self._price_levels.keys())
                volume = self._price_levels[price_level].total_volume()
                return (price_level, volume)
            else:
                return (None, None)
        elif self._order_side == OrderSide.SELL:
            if len(self._price_levels) > 0:
                price_level = min(self._price_levels.keys())
                volume = self._price_levels[price_level].total_volume()
                return (price_level, volume)
            else:
                return (None, None)

