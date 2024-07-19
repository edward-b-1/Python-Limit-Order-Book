
from lib_webserver.webserver_types import FastAPI_TopOfBook

from lib_financial_exchange.financial_exchange_types import TopOfBook


def convert_top_of_book_to_fastapi_top_of_book(top_of_book: TopOfBook) -> FastAPI_TopOfBook:

    ticker = top_of_book._ticker.to_str()

    price_buy = None if top_of_book._int_price_buy is None else top_of_book._int_price_buy.to_int()
    price_sell = None if top_of_book._int_price_sell is None else top_of_book._int_price_sell.to_int()
    volume_buy = None if top_of_book._volume_buy is None else top_of_book._volume_buy.to_int()
    volume_sell = None if top_of_book._volume_sell is None else top_of_book._volume_sell.to_int()

    fastapi_top_of_book = FastAPI_TopOfBook(
        ticker=ticker,
        price_buy=price_buy,
        volume_buy=volume_buy,
        price_sell=price_sell,
        volume_sell=volume_sell,
    )
    return fastapi_top_of_book
