
from enum import StrEnum

class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"

    # def __str__(self) -> str:
    #     return str(self.name)

    def other_side(self) :
        if self == OrderSide.BUY:
            return OrderSide.SELL
        elif self == OrderSide.SELL:
            return OrderSide.BUY
        else:
            raise RuntimeError(f'invalid OrderSide internal state')
