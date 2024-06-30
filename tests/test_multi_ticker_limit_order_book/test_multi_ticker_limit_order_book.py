
from limit_order_book.types.order_id import OrderId
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.ticker import Ticker
from limit_order_book.order import Order
from limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


def test_multi_limit_order_book_update_order_wrong_ticker():

    lob = MultiTickerLimitOrderBook()
    order_side = OrderSide("BUY")

    order_1 = Order(
        order_id=OrderId(1),
        ticker=Ticker('PYTH'),
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    order_2 = Order(
        order_id=OrderId(2),
        ticker=Ticker('RUST'),
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    order = lob.update(order_2)
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1


def test_multi_limit_order_book_update_order_wrong_order_side():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide("BUY"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide("SELL"),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    order = lob.update(order_2)
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1

