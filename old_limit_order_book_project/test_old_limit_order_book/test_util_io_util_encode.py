
from old_limit_order_book.trade import Trade

from util_io.util_encode import convert_int_price_to_price_string
from util_io.util_encode import _encode_trade
from util_io.util_encode import encode_trades


def test_convert_int_price_to_price_string_1():
    result = convert_int_price_to_price_string(1)
    assert result == '0.0001', (
        f'test_convert_int_price_to_price_string_1 failed, expected 0.0001, got {result}'
    )


def test_encode_trade_1():
    trade = Trade(
        order_id_maker=1,
        order_id_taker=2,
        ticker='PYTH',
        int_price=10000000,
        volume=10,
    )

    encoded_trade = _encode_trade(trade)
    expected_encoded_trade = f'PYTH,1000,10,2,1'
    assert encoded_trade == expected_encoded_trade, 'test_encode_trade_1 failed'


def test_encode_trade_list_1():
    trade_1 = Trade(
        order_id_maker=1,
        order_id_taker=2,
        ticker='PYTH',
        int_price=10000000,
        volume=10,
    )
    trade_2 = Trade(
        order_id_maker=10,
        order_id_taker=11,
        ticker='JAVA',
        int_price=12345678,
        volume=20,
    )

    trade_list = [
        trade_1,
        trade_2,
    ]

    encoded_trades = encode_trades(trade_list)

    assert len(encoded_trades) == 2, 'unexpected number of encoded trades'
    assert encoded_trades[0] == f'PYTH,1000,10,2,1'
    assert encoded_trades[1] == f'JAVA,1234.5678,20,11,10'

