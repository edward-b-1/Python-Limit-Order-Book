
from lib_datetime.real_datetime import now as now_real
from lib_datetime.fake_datetime import now as now_fake

from datetime import datetime
from datetime import timezone

from typeguard import typechecked


def datetime_to_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def datetime_to_order_board_display_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%d %H:%M:%S.%f %z')

def string_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')


datetime_implementation_is_fake = False

@typechecked
def set_use_fake_now_implementation(use_fake_implementation: bool) -> None:
    global datetime_implementation_is_fake
    datetime_implementation_is_fake = use_fake_implementation

def now() -> datetime:
    if datetime_implementation_is_fake:
        return now_fake()
    else:
        return now_real()

