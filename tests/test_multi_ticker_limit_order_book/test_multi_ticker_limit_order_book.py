
from limit_order_book.types.order_id import OrderId
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.ticker import Ticker
from limit_order_book.order import Order
from limit_order_book.multi_ticker_limit_order_book import MultiTickerLimitOrderBook


def test_multi_limit_order_book_update_order_wrong_order_id():

    lob = MultiTickerLimitOrderBook()
    ticker = Ticker('PYTH')
    order_side = OrderSide("BUY")

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    lob.insert(order_1)

    # Wrong order id, so should do nothing
    order = lob.update(
        order_id=OrderId(2),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1


def test_multi_limit_order_book_update_order_no_change():

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

    # No changes, so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(100),
        volume=Volume(10),
    )
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1


def test_multi_limit_order_book_update_order():

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

    # Changed price and volume
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(110),
        volume=Volume(12),
    )
    assert order == order_1
    assert order.to_int_price().to_int() == 110
    assert order.to_volume().to_int() == 12

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order is None


def test_multi_limit_order_book_update_order_int_price():

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

    # Wrong order side so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(110),
        volume=Volume(10),
    )
    assert order == order_1
    assert order.to_int_price().to_int() == 110

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order is None


def test_multi_limit_order_book_update_order_volume_increase():

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

    # Wrong order side so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(100),
        volume=Volume(11),
    )
    assert order == order_1
    assert order.to_volume().to_int() == 11

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order is None


def test_multi_limit_order_book_update_order_volume_decrease():

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

    # Wrong order side so should do nothing
    order = lob.update(
        order_id=OrderId(1),
        int_price=IntPrice(100),
        volume=Volume(9),
    )
    assert order is None

    order = lob.cancel(order_id=order_1.to_order_id())
    assert order == order_1
    assert order.to_volume().to_int() == 9

