

from new_limit_order_book.types.types import OrderId
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.order import Order
from new_limit_order_book.trade import Trade
from new_limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


class LimitOrderBookWrapper():

    def __init__(self) -> None:
        self._multi_ticker_limit_order_book = MultiTickerLimitOrderBook()

    def order_insert(self, order: Order) -> list[Trade]:
        (remaining_order, trades) = self._multi_ticker_limit_order_book.trade(order)
        if remaining_order.to_volume().is_not_zero():
            self._multi_ticker_limit_order_book.insert(remaining_order)
        return trades

    def order_modify(self, order: Order) -> list[Trade]:
        (remaining_order, trades) = self._multi_ticker_limit_order_book.modify(order)
        if remaining_order.to_volume().is_not_zero():
            self._multi_ticker_limit_order_book.insert(remaining_order)

    def order_cancel(self, order_id: OrderId) -> Order:
        order = self._multi_ticker_limit_order_book.cancel(order_id)
        if order.to_volume().is_not_zero():
            return order
        return None

    def get_order_by_order_id(self, order_id: OrderId) -> Order|None:


