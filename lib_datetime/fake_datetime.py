
from datetime import datetime
from datetime import timezone

current_datetime = None

def now() -> datetime:
    if current_datetime is None:
        raise RuntimeError(f'datetime not set')
    return current_datetime

def set_current_datetime(current_datetime_value: datetime) -> None:
    global current_datetime
    current_datetime = current_datetime_value
