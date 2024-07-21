
from lib_financial_exchange.financial_exchange_types.trade_id import TradeId

class TradeIdGenerator():
    def __init__(self) -> None:
        self._next_trade_id_value: int = 1

    def next(self) -> TradeId:
        trade_id = TradeId(self._next_trade_id_value)
        self._next_trade_id_value += 1
        return trade_id
