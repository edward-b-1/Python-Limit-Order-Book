

from limit_order_book.types.order_id import OrderId
from limit_order_book.order_side import OrderSide
from limit_order_book.order import Order
from limit_order_book.trade import Trade
from limit_order_book.ticker import Ticker
from limit_order_book.top_of_book import TopOfBook
from limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


class LimitOrderBook():

    def __init__(self) -> None:
        self._multi_ticker_limit_order_book = MultiTickerLimitOrderBook()

    def order_insert(self, order: Order) -> list[Trade]:
        trades = self._multi_ticker_limit_order_book.trade(order)

        if order.to_volume().is_not_zero():
            self._multi_ticker_limit_order_book.insert(order)

        return trades

    def order_modify(self, order: Order) -> list[Trade]:
        modified_order = self._multi_ticker_limit_order_book.update(order)

        if modified_order is not None:
            trades = self._multi_ticker_limit_order_book.trade(modified_order)

            if modified_order.to_volume().is_not_zero():
                self._multi_ticker_limit_order_book.insert(modified_order)

            return trades
        else:
            return []

    def order_cancel(self, order_id: OrderId) -> Order|None:
        order = self._multi_ticker_limit_order_book.cancel(order_id)

        #if order is None:
        #    raise RuntimeError(f'LimitOrderBook.cancel failed to cancel order with order id {order_id}')

        return order

    def top_of_book(self, ticker: Ticker) -> TopOfBook:
        top_of_book = self._multi_ticker_limit_order_book.top_of_book(ticker)
        return top_of_book

    def number_of_orders(self) -> int:
        number_of_orders = self._multi_ticker_limit_order_book.number_of_orders()
        return number_of_orders

