
from old_limit_order_book.order_side import OrderSide
from old_limit_order_book.double_limit_order_book import DoubleLimitOrderBook
from old_limit_order_book.trade import Trade


def check_depth_aggregated(lob: DoubleLimitOrderBook, depth: int):
    assert lob.depth_aggregated() == depth, f'unexpected depth {lob.depth_aggregated()}, expected {depth}'


def test_double_limit_order_book_input_5():
    '''
    Use the input from input5.txt as a test

    INSERT,1,FFLY,BUY,45.95,5
    INSERT,2,FFLY,BUY,45.95,6
    INSERT,3,FFLY,BUY,45.95,12
    INSERT,4,FFLY,SELL,46,8
    UPDATE,2,46,3
    INSERT,5,FFLY,SELL,45.95,1
    UPDATE,1,45.95,3
    INSERT,6,FFLY,SELL,45.95,1
    UPDATE,1,45.95,5
    INSERT,7,FFLY,SELL,45.95,1
    '''

    lob = DoubleLimitOrderBook()

    # INSERT,1,FFLY,BUY,45.95,5
    trades = lob.order_insert(order_id=1, ticker='FFLY', order_side=OrderSide.BUY, int_price=459500, volume=5)
    assert len(trades) == 0, 'trades'

    # INSERT,2,FFLY,BUY,45.95,6
    trades = lob.order_insert(order_id=2, ticker='FFLY', order_side=OrderSide.BUY, int_price=459500, volume=6)
    assert len(trades) == 0, 'trades'

    # INSERT,3,FFLY,BUY,45.95,12
    trades = lob.order_insert(order_id=3, ticker='FFLY', order_side=OrderSide.BUY, int_price=459500, volume=12)
    assert len(trades) == 0, 'trades'

    # INSERT,4,FFLY,SELL,46,8
    trades = lob.order_insert(order_id=4, ticker='FFLY', order_side=OrderSide.SELL, int_price=460000, volume=8)
    assert len(trades) == 0, 'trades'

    # UPDATE,2,46,3
    trades = lob.order_update(order_id=2, int_price=460000, volume=3)
    assert len(trades) == 1, f'unexpected trades'
    trade = trades[0]
    expected_trade = Trade(ticker='FFLY', int_price=460000, volume=3, order_id_maker=4, order_id_taker=2)
    assert trade == expected_trade, f'{trade} != {expected_trade}'

    # INSERT,5,FFLY,SELL,45.95,1
    trades = lob.order_insert(order_id=5, ticker='FFLY', order_side=OrderSide.SELL, int_price=459500, volume=1)
    assert len(trades) == 1, f'unexpected trades'
    trade = trades[0]
    expected_trade = Trade(ticker='FFLY', int_price=459500, volume=1, order_id_maker=1, order_id_taker=5)
    assert trade == expected_trade, f'{trade} != {expected_trade}'

    # UPDATE,1,45.95,3
    trades = lob.order_update(order_id=1, int_price=459500, volume=3)
    assert len(trades) == 0, 'trades'

    # INSERT,6,FFLY,SELL,45.95,1
    trades = lob.order_insert(order_id=6, ticker='FFLY', order_side=OrderSide.SELL, int_price=459500, volume=1)
    assert len(trades) == 1, f'unexpected trades'
    trade = trades[0]
    expected_trade = Trade(ticker='FFLY', int_price=459500, volume=1, order_id_maker=1, order_id_taker=6)
    assert trade == expected_trade, f'{trade} != {expected_trade}'

    # UPDATE,1,45.95,5
    trades = lob.order_update(order_id=1, int_price=459500, volume=5)
    assert len(trades) == 0, 'trades'

    # INSERT,7,FFLY,SELL,45.95,1
    trades = lob.order_insert(order_id=7, ticker='FFLY', order_side=OrderSide.SELL, int_price=459500, volume=1)
    assert len(trades) == 1, f'unexpected trades'
    trade = trades[0]
    expected_trade = Trade(ticker='FFLY', int_price=459500, volume=1, order_id_maker=3, order_id_taker=7)
    assert trade == expected_trade, f'{trade} != {expected_trade}'



