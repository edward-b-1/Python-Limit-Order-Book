from limit_order_book.types.order_id import OrderId

class LimitOrderBookError(Exception):
    pass

class DuplicateOrderIdError(LimitOrderBookError):
    def __init__(self, order_id: OrderId) -> None:
        self._order_id = order_id

    def __str__(self) -> str:
        return f'duplicate order id {self._order_id}'

class VolumeReduceAmountTooLarge(LimitOrderBookError):
    def __init__(self, volume: int, reduce_by_volume: int) -> None:
        self._volume = volume
        self._reduce_by_volume = reduce_by_volume

    def __str__(self) -> str:
        return f'cannot reduce current volume {self._volume} by {self._reduce_by_volume}'
