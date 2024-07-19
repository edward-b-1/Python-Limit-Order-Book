
from lib_financial_exchange.financial_exchange_types import Trade
from lib_webserver.webserver_types import FastAPI_Trade


# TODO: there's a bug: fastapi trade loses timestamp information
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
