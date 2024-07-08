
from limit_order_book.trade import Trade
from limit_order_book_webserver.types import FastAPI_Trade


def convert_trades_to_fastapi_trades(trades: list[Trade]) -> list[FastAPI_Trade]:

    def convert_trade(trade: Trade) -> FastAPI_Trade:
        return FastAPI_Trade(
            order_id_maker=trade._order_id_maker.to_int(),
            order_id_taker=trade._order_id_taker.to_int(),
            ticker=trade._ticker.to_str(),
            price=trade._int_price.to_int(),
            volume=trade._volume.to_int(),
        )

    fastapi_trades = list(
        map(
            lambda trade: convert_trade(trade),
            trades,
        )
    )
    return fastapi_trades
