
from limit_order_book.types.order_id import OrderId
from limit_order_book.ticker import Ticker
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.trade import Trade
from limit_order_book.order import Order
from limit_order_book.top_of_book import TopOfBook
from limit_order_book.exceptions import DuplicateOrderIdError

from limit_order_book.double_limit_order_book import DoubleLimitOrderBook

from more_itertools import consume

from typeguard import typechecked


# ticker -> order side -> price level -> priority queue

@typechecked
class MultiTickerLimitOrderBook:

    def __init__(self):
        self._limit_order_books: dict[Ticker, DoubleLimitOrderBook] = {}

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass


    def number_of_orders(self) -> int:
        return (
            sum(
                map(
                    lambda limit_order_book: limit_order_book.number_of_orders(),
                    self._limit_order_books.values(),
                )
            )
        )


    def trade(self, taker_order: Order) -> list[Trade]:
        ticker = taker_order.to_ticker()
        self._initialize_ticker(ticker)

        trades = self._limit_order_books[ticker].trade(taker_order)
        return trades


    def insert(self, order: Order) -> None:
        ticker = order.to_ticker()
        self._initialize_ticker(ticker)

        order_id = order.to_order_id()

        if self.order_id_exists(order_id):
            raise DuplicateOrderIdError(order_id)

        self._limit_order_books[ticker].insert(order)

    '''
    Note that 3 `update` functions are provided. This is to make the API hard
    to use incorrectly, although the implementations are similar.
    '''


    def update(self, order_id: OrderId, int_price: IntPrice, volume: Volume) -> Order|None:
        modified_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda limit_order_book: limit_order_book.update(order_id, int_price, volume),
                        self._limit_order_books.values(),
                    )
                )
            )
        )
        assert len(modified_orders) <= 1, f'MultiTickerLimitOrderBook.update invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    def update_int_price(self, order_id: OrderId, int_price: IntPrice) -> Order|None:
        modified_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda limit_order_book: limit_order_book.update_int_price(order_id, int_price),
                        self._limit_order_books.values(),
                    )
                )
            )
        )
        assert len(modified_orders) <= 1, f'MultiTickerLimitOrderBook.update_int_price invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    def update_volume(self, order_id: OrderId, volume: Volume) -> Order|None:
        modified_orders = (
            list(
                filter(
                    lambda order: order is not None,
                    map(
                        lambda limit_order_book: limit_order_book.update_volume(order_id, volume),
                        self._limit_order_books.values(),
                    )
                )
            )
        )
        assert len(modified_orders) <= 1, f'MultiTickerLimitOrderBook.update_volume invalid number of modified orders'
        if len(modified_orders) == 1:
            return modified_orders[0]
        return None


    def cancel(self, order_id: OrderId) -> Order|None:
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


    def cancel_partial(self, order_id: OrderId, volume: Volume) -> None:
        consume(
            map(
                lambda double_limit_order_book: double_limit_order_book.cancel_partial(order_id, volume),
                self._limit_order_books.values(),
            )
        )


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
            #print(f'initialize ticker {ticker}')
            self._limit_order_books[ticker] = DoubleLimitOrderBook(ticker)


    def top_of_book(self, ticker: Ticker) -> TopOfBook:
        self._initialize_ticker(ticker)

        top_of_book = self._limit_order_books[ticker].top_of_book()
        return top_of_book

    def _get_all_tickers(self) -> list[str]:
        tickers = (
            list(
                map(
                    lambda ticker: ticker.to_str(),
                    self._limit_order_books.keys(),
                )
            )
        )
        return tickers

