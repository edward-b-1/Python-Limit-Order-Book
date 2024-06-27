
from new_limit_order_book.types.order_id import OrderId
from new_limit_order_book.ticker import Ticker
from new_limit_order_book.types.int_price import IntPrice
from new_limit_order_book.types.volume import Volume
from new_limit_order_book.order_side import OrderSide
from new_limit_order_book.trade import Trade
from new_limit_order_book.order import Order

from new_limit_order_book.double_limit_order_book import DoubleLimitOrderBook



# ticker -> order side -> price level -> priority queue


class MultiTickerLimitOrderBook:

    def __init__(self):
        self._limit_order_books = dict()

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass

    def trade(self, taker_order: Order) -> list[Trade]:
        ticker = taker_order.to_ticker()
        self._initialize_ticker(ticker)

        trades = self._limit_order_books[ticker].trade(taker_order)
        return trades

    def insert(self, order: Order) -> None:
        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise RuntimeError(f'cannot insert order with existing order id {order_id}')

        ticker = order.to_ticker()
        self._limit_order_books[ticker].insert(order)

    def update(self, order: Order) -> Order|None:
        price_level_changed_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda double_limit_order_book: double_limit_order_book.update(order),
                        self._limit_order_books.values(),
                    )
                )
            )
        )

        # the above filter logic means that this is actually not possible
        assert len(price_level_changed_orders) <= 1, f'MultiTickerLimitOrderBook.update invalid number of modified price level orders'
        if len(price_level_changed_orders) == 1:
            return price_level_changed_orders[0]
        return None

    def cancel(self, order_id: OrderId) -> Order:
        cancelled_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda double_limit_order_book: double_limit_order_book.cancel(order_id),
                        self._limit_order_books.values(),
                    )
                )
            )
        )

        assert len(cancelled_orders) <= 1, f'MultiTickerLimitOrderBook.cancel invalid number of orders'
        if len(cancelled_orders) == 1:
            return cancelled_orders[0]
        return None

    def order_id_exists(self, order_id: OrderId) -> bool:
        matching_limit_order_books = (
            list(
                filter(
                    lambda order_id_exists_bool: order_id_exists_bool == True,
                    map(
                        lambda double_limit_order_book: double_limit_order_book.order_id_exists(order_id),
                        self._limit_order_books.values(),
                    )
                )
            )
        )

        assert len(matching_limit_order_books) <= 1, f'MultiTickerLimitOrderBook.order_id_exists invalid number of matching tickers'
        return len(matching_limit_order_books) == 1


    def _initialize_ticker(self, ticker: Ticker) -> None:
        if not ticker in self._limit_order_books:
            self._limit_order_books[ticker] = DoubleLimitOrderBook(ticker)