
from datetime import datetime
from datetime import timezone


def datetime_to_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def datetime_to_order_board_display_string(now: datetime) -> str:
    return now.strftime('%Y-%m-%d %H:%M:%S.%f %z')

def string_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')

