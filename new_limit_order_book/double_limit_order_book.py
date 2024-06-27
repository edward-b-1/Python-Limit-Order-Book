
from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.types.int_price import IntPrice
from new_limit_order_book.types.volume import Volume
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.trade import Trade
from new_limit_order_book.order import Order

from new_limit_order_book.single_side_limit_order_book import SingleSideLimitOrderBook

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


    def trade(self, taker_order: Order) -> list[Trade]:
        assert taker_order.to_ticker() == self._ticker, f'DoubleLimitOrderBook.trade ticker mismatch'

        order_side = taker_order.to_order_side()
        other_side_order_side = order_side.other_side()

        other_side_limit_order_book = self._limit_order_book[other_side_order_side]
        trades = other_side_limit_order_book.trade(taker_order)
        return trades


    def insert(self, order: Order) -> None:
        assert order.to_ticker() == self._ticker, f'DoubleLimitOrderBook.insert ticker mismatch'

        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise RuntimeError(f'duplicate order id {order_id}')

        order_side = order.to_order_side()

        self._limit_order_book[order_side].insert(order)


    def update(self, order: Order) -> Order|None:
        assert order.to_ticker() == self._ticker, f'DoubleLimitOrderBook.update ticker mismatch'

        price_level_changed_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda single_side_limit_order_book: single_side_limit_order_book.update(order),
                        self._limit_order_book.values(),
                    )
                )
            )
        )

        # the above filter logic means that this is actually not possible
        assert len(price_level_changed_orders) <= 1, f'DoubleLimitOrderBook.update invalid number of modified price level orders'
        if len(price_level_changed_orders) == 1:
            return price_level_changed_orders[0]
        return None


    def cancel(self, order_id: OrderId) -> Order:
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

