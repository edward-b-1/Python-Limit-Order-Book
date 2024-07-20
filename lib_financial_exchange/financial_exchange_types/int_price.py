
from functools import total_ordering

@total_ordering
class IntPrice():

    def __init__(self, int_price: int) -> None:
        assert int_price >= 0, f'IntPrice.__init__ negative int price not valid'
        self._int_price = int_price

    def __hash__(self) -> int:
        return hash(self._int_price)

    def __str__(self) -> str:
        return f'IntPrice({self._int_price})'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, IntPrice):
            return self._int_price == value._int_price
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, IntPrice):
            return self._int_price < other._int_price
        raise NotImplementedError(f'not implemented')

    # def __ge__(self, other: object) -> bool:
    #     return not self.__lt__(other)

    # def __gt__(self, other: object) -> bool:
    #     if isinstance(other, IntPrice):
    #         return self._int_price > other._int_price
    #     raise NotImplementedError(f'not implemented')

    # def __le__(self, other: object) -> bool:
    #     return not self.__gt__(other)

    def to_int(self) -> int:
        return self._int_price