
from datetime import datetime
from datetime import timezone


def now() -> datetime:
    return datetime.now(timezone.utc)

def now_string() -> str:
    datetime_now = now()
    return datetime_to_string(datetime_now)

def datetime_to_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def string_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')