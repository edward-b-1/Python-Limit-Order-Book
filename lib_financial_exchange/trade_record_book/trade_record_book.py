
from lib_financial_exchange.financial_exchange_types import Trade

from typeguard import typechecked

@typechecked
class TradeRecordBook():

    def __init__(self) -> None:
        self._trades: list[Trade] = []

    def add_trade(self, trade: Trade) -> None:
        self._trades.append(trade)

    def add_trades(self, trades: list[Trade]) -> None:
        self._trades += trades

    def get_trades(self) -> list[Trade]:
        return self._trades

    # TODO: add statistics eg total volume traded on each instrument
    # per hour, day