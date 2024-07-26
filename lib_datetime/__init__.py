
from datetime import datetime
from datetime import timezone

from typeguard import typechecked


@typechecked
class DatetimeProxy():
    def __init__(self) -> None:
        pass

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def now_string(self) -> str:
        datetime_now = self.now()
        return datetime_to_string(datetime_now)


@typechecked
class FakeDatetimeProxy():
    def __init__(self, current_datetime: datetime) -> None:
        self._datetime = current_datetime

    def set_datetime(self, current_datetime: datetime) -> None:
        self._datetime = current_datetime

    def now(self) -> datetime:
        return self._datetime

    def now_string(self) -> str:
        datetime_now = self.now()
        return datetime_to_string(datetime_now)


@typechecked
class DatetimeStrategy():
    def __init__(
        self,
        test_mode: bool = False,
        current_datetime: datetime|None = None,
    ) -> None:
        if test_mode:
            if current_datetime is None:
                fixed_datetime = (
                    datetime(
                        year=2024, month=1, day=1,
                        hour=9, minute=30, second=0,
                        tzinfo=timezone.utc,
                    )
                )
                self._datetime_strategy = (
                    FakeDatetimeProxy(current_datetime=fixed_datetime)
                )
            else:
                self._datetime_strategy = (
                    FakeDatetimeProxy(current_datetime=current_datetime)
                )
        else:
            self._datetime_strategy = DatetimeProxy()

    def set_datetime(self, current_datetime: datetime) -> None:
        if isinstance(self._datetime_strategy, FakeDatetimeProxy):
            self._datetime_strategy.set_datetime(current_datetime=current_datetime)
        else:
            raise NotImplementedError(f'cannot call set_datetime on object of type {type(self._datetime_strategy)}')

    def now(self) -> datetime:
        print(f'DatetimeStrategy.now(): {type(self._datetime_strategy)} -> {self._datetime_strategy.now()}')
        return self._datetime_strategy.now()

    def now_string(self) -> str:
        print(f'DatetimeStrategy.now_string(): {type(self._datetime_strategy)} -> {self._datetime_strategy.now_string()}')
        return self._datetime_strategy.now_string()


def datetime_to_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def datetime_to_order_board_display_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%d %H:%M:%S.%f %z')

def string_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')

