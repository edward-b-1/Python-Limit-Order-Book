
from enum import Enum

class OrderSide(Enum):
    BUY = 1
    SELL = 2

    def __str__(self) -> str:
        return str(self.name)

    def other_side(self) :
        if self == OrderSide.BUY:
            return OrderSide.SELL
        elif self == OrderSide.SELL:
            return OrderSide.BUY
        else:
            raise RuntimeError(f'invalid OrderSide internal state')
