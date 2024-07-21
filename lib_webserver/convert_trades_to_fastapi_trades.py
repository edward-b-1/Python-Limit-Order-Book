
from lib_financial_exchange.financial_exchange_types import Trade
from lib_webserver.webserver_types import FastAPI_Trade

from lib_datetime import datetime_to_order_board_display_string


def convert_trades_to_fastapi_trades(trades: list[Trade]) -> list[FastAPI_Trade]:

    def convert_trade(trade: Trade) -> FastAPI_Trade:
        return FastAPI_Trade(
            trade_id=trade.to_trade_id().to_int(),
            order_id_maker=trade.order_id_maker().to_int(),
            order_id_taker=trade.order_id_taker().to_int(),
            timestamp=datetime_to_order_board_display_string(trade.to_timestamp()),
            ticker=trade.to_ticker().to_str(),
            price=trade.to_int_price().to_int(),
            volume=trade.to_volume().to_int(),
        )

    fastapi_trades = list(
        map(
            lambda trade: convert_trade(trade),
            trades,
        )
    )
    return fastapi_trades
