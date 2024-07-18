
import logging
import sys
from datetime import datetime
from datetime import timezone


PROCESS_NAME = 'limit_order_book'


log = logging.getLogger(PROCESS_NAME)

stdout_log_formatter = logging.Formatter(
    '%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d | %(message)s'
)
stdout_log_handler = logging.StreamHandler(stream=sys.stdout)
stdout_log_handler.setLevel(logging.INFO)
stdout_log_handler.setFormatter(stdout_log_formatter)

file_log_formatter = logging.Formatter(
    '%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d | %(message)s'
)
file_log_handler = logging.FileHandler(
    filename=f'{PROCESS_NAME}_{datetime.now(timezone.utc).date()}.log'
)
file_log_handler.setLevel(logging.DEBUG)
file_log_handler.setFormatter(file_log_formatter)

log.setLevel(logging.DEBUG)
log.addHandler(stdout_log_handler)
log.addHandler(file_log_handler)
