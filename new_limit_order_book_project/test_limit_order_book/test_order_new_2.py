
from limit_order_book.ticker import Ticker
from limit_order_book.types.order_id import OrderId
from limit_order_book.types.int_price import IntPrice
from limit_order_book.types.volume import Volume
from limit_order_book.order_side import OrderSide
from limit_order_book.trade import Trade
from limit_order_book.order import Order

# TODO: write the tests for match and finish the match function
# should test prices which do not match
# prices which match
# prices which cross through
# same volume
# asymetric volume (both ways)

# 1/1
# Test no matching order for different ticker
def test_order_no_match_different_ticker():
    int_price = IntPrice(1000)
    volume = Volume(10)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=Ticker('PYTH'),
        order_side=OrderSide.BUY,
        int_price=int_price,
        volume=volume,
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=Ticker('JAVA'),
        order_side=OrderSide.SELL,
        int_price=int_price,
        volume=volume,
    )

    trade = order_1.match(order_2)
    assert trade == None, f'unexpected order match'


# 1/1
# Test no matching order for same order_side
def test_order_no_match_same_order_side():
    ticker = Ticker('PYTH')
    order_side = OrderSide.BUY
    int_price = IntPrice(1000)
    volume = Volume(10)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=volume,
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=order_side,
        int_price=int_price,
        volume=volume,
    )

    trade = order_1.match(order_2)
    assert trade == None, f'unexpected order match'

# 1/1
# Test no matching order for incompatiable int_price
def test_order_no_match_no_match_price():
    ticker = Ticker('PYTH')
    volume = Volume(10)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(1000),
        volume=volume,
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1010),
        volume=volume,
    )

    trade = order_1.match(order_2)
    assert trade == None, f'unexpected order match'

# 1/3
# Test fully matched order for compatiable int_price
def test_order_full_match_same_price():
    ticker = Ticker('PYTH')
    int_price = IntPrice(1000)
    volume = Volume(10)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=int_price,
        volume=volume,
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=int_price,
        volume=volume,
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=int_price,
        volume=volume
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'

# 2/3
# Test partially matched maker order for compatiable int_price
def test_order_partial_maker_match_same_price():
    ticker = Ticker('PYTH')
    int_price = IntPrice(1000)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=int_price,
        volume=Volume(20)
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=int_price,
        volume=Volume(10),
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=int_price,
        volume=Volume(10),
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'
    assert order_1.to_volume() == Volume(10), f'unexpected maker order volume'
    assert order_2.to_volume() == Volume(0), f'unexpected taker order volume'

# 3/3
# Test partially matched taker order for compatiable int_price
def test_order_partial_taker_match_same_price():
    ticker = Ticker('PYTH')
    int_price = IntPrice(1000)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=int_price,
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=int_price,
        volume=Volume(20),
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=int_price,
        volume=Volume(10),
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'
    assert order_1.to_volume() == Volume(0), f'unexpected maker order volume'
    assert order_2.to_volume() == Volume(10), f'unexpected taker order volume'

# 1/3
# Test fully matched order for crossing taker price
def test_order_full_match_crossing_taker_price():
    ticker = Ticker('PYTH')
    volume = Volume(10)

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(2000),
        volume=volume,
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1000),
        volume=volume,
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=IntPrice(1000),
        volume=volume,
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'

# 2/3
# Test partially matched maker order for crossing taker price
def test_order_partial_maker_match_crossing_taker_price():
    ticker = Ticker('PYTH')

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(2000),
        volume=Volume(20),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1000),
        volume=Volume(10),
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=IntPrice(1000),
        volume=Volume(10),
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'
    assert order_1.to_volume() == Volume(10), f'unexpected maker order volume'
    assert order_2.to_volume() == Volume(0), f'unexpected taker order volume'

# 3/3
# Test partially matched taker order for crossing taker price
def test_order_partial_taker_match_crossing_taker_price():
    ticker = Ticker('PYTH')

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(2000),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1000),
        volume=Volume(20),
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=IntPrice(1000),
        volume=Volume(10),
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'
    assert order_1.to_volume() == Volume(0), f'unexpected maker order volume'
    assert order_2.to_volume() == Volume(10), f'unexpected taker order volume'

# 1/3
# Test fully matched order for crossing taker price (reversed)
def test_order_full_match_crossing_taker_price_reversed():
    ticker = Ticker('PYTH')
    volume = Volume(10)

    order_maker = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1000),
        volume=volume,
    )

    order_taker = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(2000),
        volume=volume,
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=IntPrice(2000),
        volume=volume
    )

    trade = order_maker.match(order_taker)
    print(expected_trade)
    print(trade)
    assert trade == expected_trade, f'unexpected trade data or no trade'

# 2/3
# Test partially matched maker order for crossing taker price (reversed)
def test_order_partial_maker_match_crossing_taker_price_reversed():
    ticker = Ticker('PYTH')

    maker_order = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1000),
        volume=Volume(20),
    )

    taker_order = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(2000),
        volume=Volume(10),
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=IntPrice(2000),
        volume=Volume(10),
    )

    trade = maker_order.match(taker_order)
    assert trade == expected_trade, f'unexpected trade data or no trade'
    assert maker_order.to_volume() == Volume(10), f'unexpected maker order volume'
    assert taker_order.to_volume() == Volume(0), f'unexpected taker order volume'

# 3/3
# Test partially matched taker order for crossing taker price (reversed)
def test_order_partial_taker_match_crossing_taker_price_reversed():
    ticker = Ticker('PYTH')

    order_1 = Order(
        order_id=OrderId(1),
        ticker=ticker,
        order_side=OrderSide.SELL,
        int_price=IntPrice(1000),
        volume=Volume(10),
    )

    order_2 = Order(
        order_id=OrderId(2),
        ticker=ticker,
        order_side=OrderSide.BUY,
        int_price=IntPrice(2000),
        volume=Volume(20),
    )

    expected_trade = Trade(
        order_id_maker=OrderId(1),
        order_id_taker=OrderId(2),
        ticker=ticker,
        int_price=IntPrice(2000),
        volume=Volume(10),
    )

    trade = order_1.match(order_2)
    assert trade == expected_trade, f'unexpected trade data or no trade'
    assert order_1.to_volume() == Volume(0), f'unexpected maker order volume'
    assert order_2.to_volume() == Volume(10), f'unexpected taker order volume'

