

from old_limit_order_book.order_side import OrderSide

VALIDATE_ORDER_ID_ERROR_STR = 'order_id cannot be negative'
VALIDATE_TICKER_ERROR_STR = 'ticker cannot be empty string'
VALIDATE_ORDER_SIDE_ERROR_STR = 'invalid order side'
VALIDATE_INT_PRICE_ERROR_STR = 'int_price must be non-negative'
VALIDATE_VOLUME_ERROR_STR = 'volume must be positive'

def validate_order_id(order_id: int) -> bool:
    return order_id >= 0

def validate_ticker(ticker: str) -> bool:
    return len(ticker) > 0

def validate_order_side(order_side: str) -> bool:
    return order_side == OrderSide.BUY or order_side == OrderSide.SELL

def validate_int_price(int_price: int) -> bool:
    return int_price >= 0

def validate_volume(volume: int) -> bool:
    return volume > 0

__all__ = [
    'VALIDATE_ORDER_ID_ERROR_STR',
    'VALIDATE_TICKER_ERROR_STR',
    'VALIDATE_ORDER_SIDE_ERROR_STR',
    'VALIDATE_INT_PRICE_ERROR_STR',
    'VALIDATE_VOLUME_ERROR_STR',
    'validate_order_id',
    'validate_ticker',
    'validate_order_side',
    'validate_int_price',
    'validate_volume',
]
