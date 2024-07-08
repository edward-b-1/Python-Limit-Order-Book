
from limit_order_book.ticker import Ticker
from limit_order_book_webserver.types import FastAPI_Ticker


def convert_ticker_list_to_fastapi_ticker_list(ticker_list: list[Ticker]) -> list[str]:
    fastapi_ticker_list = list(
        map(
            lambda ticker: ticker.to_str(),
            ticker_list,
        )
    )
    return fastapi_ticker_list
