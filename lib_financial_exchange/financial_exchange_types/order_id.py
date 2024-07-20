
from functools import total_ordering

@total_ordering
class OrderId():

    def __init__(self, order_id: int) -> None:
        assert order_id >= 0, f'OrderId.__init__ negative order_id not valid'
        self._order_id = order_id

    def __hash__(self) -> int:
        return hash(self._order_id)

    def __str__(self) -> str:
        return f'OrderId({self._order_id})'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, OrderId):
            return self._order_id == value._order_id
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, OrderId):
            return self._order_id < other._order_id
        raise NotImplementedError(f'not implemented: {type(self)} < {type(other)}')

    # def __ge__(self, other: object) -> bool:
    #     return not self.__lt__(other)

    # def __gt__(self, other: object) -> bool:
    #     if isinstance(other, OrderId):
    #         return self._order_id > other._order_id
    #     raise NotImplementedError(f'not implemented: {type(self)} > {type(other)}')

    # def __le__(self, other: object) -> bool:
    #     return not self.__gt__(other)

    def to_int(self) -> int:
        return self._order_id
