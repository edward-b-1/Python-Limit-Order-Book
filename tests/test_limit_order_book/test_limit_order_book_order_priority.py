
from lib_financial_exchange.financial_exchange_types import ClientName
from lib_financial_exchange.financial_exchange_types import OrderId
from lib_financial_exchange.financial_exchange_types import IntPrice
from lib_financial_exchange.financial_exchange_types import Volume
from lib_financial_exchange.financial_exchange_types import OrderSide
from lib_financial_exchange.financial_exchange_types import Ticker
from lib_financial_exchange.financial_exchange_types import OrderInsertMessage
from lib_financial_exchange.financial_exchange_types import Order
from lib_financial_exchange.financial_exchange_types import Trade
from lib_financial_exchange.financial_exchange_types import TopOfBook
from lib_financial_exchange.limit_order_book import LimitOrderBook

from datetime import datetime


def inspect_order_queue(limit_order_book: LimitOrderBook, ticker: Ticker, int_price: IntPrice) -> list[Order]:
    return (
        limit_order_book
        ._multi_ticker_limit_order_book
        ._limit_order_books[ticker]
        ._buy_side_limit_order_book
        ._price_levels[int_price]
        ._queue
    )


def inspect_order_queue_length(limit_order_book: LimitOrderBook, ticker: Ticker, int_price: IntPrice) -> int:
    return (
        len(
            inspect_order_queue(limit_order_book, ticker, int_price)
        )
    )


def inspect_order_queue_element(limit_order_book: LimitOrderBook, ticker: Ticker, int_price: IntPrice, index: int) -> Order:
    return (
        inspect_order_queue(limit_order_book, ticker, int_price)[index]
    )


def order_from_order_without_order_id(
    order_without_order_id: OrderInsertMessage,
    order_id: OrderId,
) -> Order:
    return Order(
        order_id=order_id,
        ticker=order_without_order_id.to_ticker(),
        order_side=order_without_order_id.to_order_side(),
        int_price=order_without_order_id.to_int_price(),
        volume=order_without_order_id.to_volume(),
    )


def create_limit_order_book(ticker, order_side, int_price, int_price_2) -> tuple[LimitOrderBook, list[Order], list[OrderId]]:

    lob = LimitOrderBook()
    client_name = ClientName(client_name='test')
    timestamp = datetime(year=2024, month=7, day=11)

    ####

    order_1 = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(10),
    )
    (order_id_1, trades) = lob.order_insert(order_1)
    assert trades == []
    assert inspect_order_queue_length(lob, ticker, int_price) == 1
    assert inspect_order_queue_element(lob, ticker, int_price, 0) == order_from_order_without_order_id(order_1, order_id_1)

    ####

    order_2 = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=Volume(20),
    )
    (order_id_2, trades) = lob.order_insert(order_2)
    assert trades == []
    assert inspect_order_queue_length(lob, ticker, int_price) == 2
    assert inspect_order_queue_element(lob, ticker, int_price, 0) == order_from_order_without_order_id(order_1, order_id_1)
    assert inspect_order_queue_element(lob, ticker, int_price, 1) == order_from_order_without_order_id(order_2, order_id_2)

    #### insert another order into different price level

    order_3 = OrderInsertMessage(
        client_name=client_name,
        timestamp=timestamp,
        ticker=ticker,
        order_side=order_side,
        int_price=int_price_2,
        volume=Volume(1),
    )
    (order_id_3, trades) = lob.order_insert(order_3)
    assert trades == []
    assert inspect_order_queue_length(lob, ticker, int_price) == 2
    assert inspect_order_queue_element(lob, ticker, int_price, 0) == order_from_order_without_order_id(order_1, order_id_1)
    assert inspect_order_queue_element(lob, ticker, int_price, 1) == order_from_order_without_order_id(order_2, order_id_2)
    assert inspect_order_queue_length(lob, ticker, int_price_2) == 1
    assert inspect_order_queue_element(lob, ticker, int_price_2, 0) == order_from_order_without_order_id(order_3, order_id_3)

    return (lob, [order_1, order_2, order_3], [order_id_1, order_id_2, order_id_3])


def test_limit_order_book_order_priority_decrease_volume():

    ticker = Ticker('NVDA')
    order_side = OrderSide('BUY')
    int_price = IntPrice(1000)
    int_price_2 = IntPrice(1010)
    (lob, orders, order_ids) = create_limit_order_book(ticker, order_side, int_price, int_price_2)
    order_1 = orders[0]
    order_2 = orders[1]
    order_3 = orders[2]
    order_id_1 = order_ids[0]
    order_id_2 = order_ids[1]
    order_id_3 = order_ids[2]

    ####

    order_1_2 = Order(
        order_id_1,
        ticker,
        order_side,
        int_price,
        volume=Volume(9),
    )

    trades = lob.order_update(order_id_1, int_price, volume=Volume(9))
    assert trades == []
    assert inspect_order_queue_length(lob, ticker, int_price) == 2
    assert inspect_order_queue_element(lob, ticker, int_price, 0) == order_from_order_without_order_id(order_1_2, order_id_1)
    assert inspect_order_queue_element(lob, ticker, int_price, 1) == order_from_order_without_order_id(order_2, order_id_2)
    assert inspect_order_queue_length(lob, ticker, int_price_2) == 1
    assert inspect_order_queue_element(lob, ticker, int_price_2, 0) == order_from_order_without_order_id(order_3, order_id_3)


def test_limit_order_book_order_priority_increase_volume():

    ticker = Ticker('NVDA')
    order_side = OrderSide('BUY')
    int_price = IntPrice(1000)
    int_price_2 = IntPrice(1010)
    (lob, orders, order_ids) = create_limit_order_book(ticker, order_side, int_price, int_price_2)
    order_1 = orders[0]
    order_2 = orders[1]
    order_3 = orders[2]
    order_id_1 = order_ids[0]
    order_id_2 = order_ids[1]
    order_id_3 = order_ids[2]

    ####

    order_1_2 = Order(
        order_id_1,
        ticker,
        order_side,
        int_price,
        volume=Volume(11),
    )

    trades = lob.order_update(order_id_1, int_price, volume=Volume(11))
    assert trades == []
    assert inspect_order_queue_length(lob, ticker, int_price) == 2
    assert inspect_order_queue_element(lob, ticker, int_price, 0) == order_from_order_without_order_id(order_2, order_id_2), f'order has not changed priority'
    assert inspect_order_queue_element(lob, ticker, int_price, 1) == order_from_order_without_order_id(order_1_2, order_id_1), f'order has not changed priority'
    assert inspect_order_queue_length(lob, ticker, int_price_2) == 1
    assert inspect_order_queue_element(lob, ticker, int_price_2, 0) == order_from_order_without_order_id(order_3, order_id_3)


def test_limit_order_book_order_priority_change_int_price():

    ticker = Ticker('NVDA')
    order_side = OrderSide('BUY')
    int_price = IntPrice(1000)
    int_price_2 = IntPrice(1010)
    (lob, orders, order_ids) = create_limit_order_book(ticker, order_side, int_price, int_price_2)
    order_1 = orders[0]
    order_2 = orders[1]
    order_3 = orders[2]
    order_id_1 = order_ids[0]
    order_id_2 = order_ids[1]
    order_id_3 = order_ids[2]

    ####

    order_1_2 = Order(
        order_id_1,
        ticker,
        order_side,
        int_price=IntPrice(1010),
        volume=Volume(10),
    )

    trades = lob.order_update(order_id_1, int_price=IntPrice(1010), volume=Volume(10))
    assert trades == []
    assert inspect_order_queue_length(lob, ticker, int_price) == 1
    assert inspect_order_queue_element(lob, ticker, int_price, 0) == order_from_order_without_order_id(order_2, order_id_2), f'order has not changed priority'
    assert inspect_order_queue_length(lob, ticker, int_price_2) == 2
    assert inspect_order_queue_element(lob, ticker, int_price_2, 0) == order_from_order_without_order_id(order_3, order_id_3)
    assert inspect_order_queue_element(lob, ticker, int_price_2, 1) == order_from_order_without_order_id(order_1_2, order_id_1), f'order has not changed priority'


