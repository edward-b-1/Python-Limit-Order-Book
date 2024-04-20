
from limit_order_book.trade import Trade


def convert_int_price_to_price_string(int_price: int) -> str:
    # TODO: throw error if len(remainder) > 4
    integer_price = int_price // 10000
    remainder_price = int_price % 10000
    float_format_price = f'{integer_price}.{remainder_price:04d}' if remainder_price != 0 else f'{integer_price}'
    return float_format_price


def _encode_trade(trade: Trade) -> str:
    symbol = trade.ticker
    int_price = trade.int_price
    volume = trade.volume
    taker_order_id = trade.order_id_taker
    maker_order_id = trade.order_id_maker

    # convert the price to a string in the required format
    price_string = convert_int_price_to_price_string(int_price)

    return (
        f'{symbol},{price_string},{volume},{taker_order_id},{maker_order_id}'
    )


def encode_trades(trades: list[Trade]) -> list[str]:

    trade_report = []
    for trade in trades:
        trade_report.append(
            _encode_trade(trade)
        )
    return trade_report