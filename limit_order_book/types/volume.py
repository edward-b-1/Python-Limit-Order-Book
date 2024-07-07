
from limit_order_book.exceptions import VolumeReduceAmountTooLarge


class Volume():

    def __init__(self, volume: int) -> None:
        assert volume >= 0, f'Volume.__init__ negative volume not valid'
        self._volume = volume

    def __str__(self) -> str:
        return f'Volume({self._volume})'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Volume):
            return self._volume == value._volume
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Volume):
            return self._volume < other._volume
        raise NotImplementedError(f'not implemented')

    def __ge__(self, other: object) -> bool:
        return not self.__lt__(other)

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Volume):
            return self._volume > other._volume
        raise NotImplementedError(f'not implemented')

    def __le__(self, other: object) -> bool:
        return not self.__gt__(other)

    def __sub__(self, other: object):
        if isinstance(other, Volume):
            volume = self._volume - other._volume
            return Volume(volume=volume)
        raise TypeError(f'cannot subtract {type(other)} from {type(Volume)}')

    def reduce(self, volume) -> None:
        if volume > self:
            raise VolumeReduceAmountTooLarge(volume=self.to_int(), reduce_by_volume=volume.to_int())

    def is_zero(self) -> bool:
        return self._volume == 0

    def is_not_zero(self) -> bool:
        return not self.is_zero()

    def to_int(self) -> int:
        return self._volume