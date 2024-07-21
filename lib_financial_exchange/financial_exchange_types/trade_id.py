
from functools import total_ordering

@total_ordering
class TradeId():

    def __init__(self, trade_id: int) -> None:
        assert trade_id >= 0, f'TradeId.__init__ negative order_id not valid'
        self._trade_id = trade_id

    def __hash__(self) -> int:
        return hash(self._trade_id)

    def __str__(self) -> str:
        return f'TradeId({self._trade_id})'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, TradeId):
            return self._trade_id == value._trade_id
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, TradeId):
            return self._trade_id < other._trade_id
        raise NotImplementedError(f'not implemented: {type(self)} < {type(other)}')

    # def __ge__(self, other: object) -> bool:
    #     return not self.__lt__(other)

    # def __gt__(self, other: object) -> bool:
    #     if isinstance(other, TradeId):
    #         return self._order_id > other._order_id
    #     raise NotImplementedError(f'not implemented: {type(self)} > {type(other)}')

    # def __le__(self, other: object) -> bool:
    #     return not self.__gt__(other)

    def to_int(self) -> int:
        return self._trade_id
