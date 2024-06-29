
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.double_limit_order_book import DoubleLimitOrderBook
from old_limit_order_book.trade import Trade


def check_depth_aggregated(lob: DoubleLimitOrderBook, depth: int):
    assert lob.depth_aggregated() == depth, f'unexpected depth {lob.depth_aggregated()}, expected {depth}'

def test_double_limit_order_book_1():
    '''
    Test inserting some orders, on both sides, which do not match on price.
    '''

    lob = DoubleLimitOrderBook()

    lob.order_insert(order_id=1, ticker='PYTH', order_side=OrderSide.BUY, int_price=1000, volume=10)
    # TODO: implement this
    #priority = lob.priority(order_id=1)
    #assert priority == 0, f'unexpected priority {priority} for order {1}, expected {0}'
    check_depth_aggregated(lob, 1)

    trades = lob.order_insert(order_id=2, ticker='PYTH', order_side=OrderSide.BUY, int_price=1000, volume=20)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 2)

    trades = lob.order_insert(order_id=3, ticker='PYTH', order_side=OrderSide.BUY, int_price=1020, volume=10)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 3)

    trades = lob.order_insert(order_id=4, ticker='PYTH', order_side=OrderSide.BUY, int_price=1020, volume=20)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 4)

    trades = lob.order_insert(order_id=5, ticker='PYTH', order_side=OrderSide.SELL, int_price=1100, volume=10)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 5)

    trades = lob.order_update(order_id=1, int_price=1000, volume=5)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 5)

    trades = lob.order_update(order_id=1, int_price=1010, volume=5)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 5)

    trades = lob.order_update(order_id=2, int_price=1010, volume=20)
    assert len(trades) == 0, f'unexpected trade'
    check_depth_aggregated(lob, 5)

    lob.order_cancel(5)
    lob.order_cancel(4)
    lob.order_cancel(3)
    lob.order_cancel(2)
    lob.order_cancel(1)
    check_depth_aggregated(lob, 0)


def test_double_limit_order_book_update_1():
    '''
    Insert buy and sell which do not match. Update the buy order so that it
    matches, causing half the sell volume to be traded.
    '''

    lob = DoubleLimitOrderBook()

    trades = lob.order_insert(order_id=1, ticker='PYTH', order_side=OrderSide.BUY, int_price=999, volume=5)
    #assert trades is None, 'trades'
    assert len(trades) == 0, 'trades'

    trades = lob.order_insert(order_id=2, ticker='PYTH', order_side=OrderSide.SELL, int_price=1000, volume=10)
    #assert trades is None, 'trades'
    assert len(trades) == 0, 'trades'

    trades = lob.order_update(order_id=1, int_price=1000, volume=5)
    assert len(trades) == 1, 'number of trades is not 1'
    trade = trades[0]
    expected_trade = Trade(
        order_id_maker=2,
        order_id_taker=1,
        ticker='PYTH',
        int_price=1000,
        volume=5,
    )
    assert trade == expected_trade, 'trade does not match expected data'


def test_double_limit_order_book_update_2():
    '''
    Insert buy and 2x sell which do not match. Update the buy order so that it
    matches, causing 1 sell order to be fully matched and half the remaining
    sell volume to be traded.
    '''

    lob = DoubleLimitOrderBook()

    trades = lob.order_insert(order_id=1, ticker='PYTH', order_side=OrderSide.BUY, int_price=999, volume=5)
    assert len(trades) == 0, 'trades'

    trades = lob.order_insert(order_id=2, ticker='PYTH', order_side=OrderSide.SELL, int_price=1000, volume=10)
    trades = lob.order_insert(order_id=3, ticker='PYTH', order_side=OrderSide.SELL, int_price=1000, volume=10)
    assert len(trades) == 0, 'trades'

    trades = lob.order_update(order_id=1, int_price=1000, volume=15)
    assert len(trades) == 2, 'number of trades is not 2'

    trade = trades[0]
    expected_trade = Trade(
        order_id_maker=2,
        order_id_taker=1,
        ticker='PYTH',
        int_price=1000,
        volume=10,
    )
    assert trade == expected_trade, 'trade does not match expected data'

    trade = trades[1]
    expected_trade = Trade(
        order_id_maker=3,
        order_id_taker=1,
        ticker='PYTH',
        int_price=1000,
        volume=5,
    )
    assert trade == expected_trade, 'trade does not match expected data'


def test_double_limit_order_book_update_3():
    '''
    Insert buy and 2x sell which do not match. Update the buy order so that it
    matches, and the price exceeds the matching level price.
    This causes 1 sell order to be fully matched and half the remaining
    sell volume to be traded. Both orders trade at the aggressor price.
    '''

    lob = DoubleLimitOrderBook()

    trades = lob.order_insert(order_id=1, ticker='PYTH', order_side=OrderSide.BUY, int_price=999, volume=5)
    assert len(trades) == 0, 'trades'

    trades = lob.order_insert(order_id=2, ticker='PYTH', order_side=OrderSide.SELL, int_price=1000, volume=10)
    trades = lob.order_insert(order_id=3, ticker='PYTH', order_side=OrderSide.SELL, int_price=1000, volume=10)
    assert len(trades) == 0, 'trades'

    trades = lob.order_update(order_id=1, int_price=1010, volume=15)
    assert len(trades) == 2, 'number of trades is not 2'

    trade = trades[0]
    expected_trade = Trade(
        order_id_maker=2,
        order_id_taker=1,
        ticker='PYTH',
        int_price=1010,
        volume=10,
    )
    assert trade == expected_trade, 'trade does not match expected data'

    trade = trades[1]
    expected_trade = Trade(
        order_id_maker=3,
        order_id_taker=1,
        ticker='PYTH',
        int_price=1010,
        volume=5,
    )
    assert trade == expected_trade, 'trade does not match expected data'

