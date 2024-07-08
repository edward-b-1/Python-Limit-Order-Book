
def helper_generate_order(order_id: int, ticker: str, order_side: str, price: int, volume: int):
    return {
        'order_id': order_id,
        'ticker': ticker,
        'order_side': order_side,
        'price': price,
        'volume': volume,
    }

def helper_generate_order_without_order_id(ticker: str, order_side: str, price: int, volume: int):
    return {
        'ticker': ticker,
        'order_side': order_side,
        'price': price,
        'volume': volume,
    }

def helper_generate_order_id_price_volume(order_id: int, price: int, volume: int):
    return {
        'order_id': order_id,
        'price': price,
        'volume': volume,
    }

def helper_generate_top_of_book(
    ticker: str,
    price_buy: int|None,
    volume_buy: int|None,
    price_sell: int|None,
    volume_sell: int|None,
):
    return {
        'status': 'success',
        'message': None,
        'top_of_book': {
            'ticker': ticker,
            'price_buy': price_buy,
            'volume_buy': volume_buy,
            'price_sell': price_sell,
            'volume_sell': volume_sell,
        }
    }

def helper_generate_ticker(
    ticker: str,
):
    return {
        'ticker': ticker,
    }

def helper_generate_order_id(
    order_id: int,
):
    return {
        'order_id': order_id,
    }