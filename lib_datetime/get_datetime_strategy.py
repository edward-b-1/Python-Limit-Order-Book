
from fastapi import Request

from lib_datetime import DatetimeStrategy

import os


# NOTE: This environment variable should NOT be set by Unit Test Code.
# It is here so that systems can switch the Webserver mode into a test mode
# so that the webserver can be deployed to UAT systems for testing.
webserver_test_mode = False
if os.environ.get('ENABLE_WEBSERVER_TEST_MODE'):
    webserver_test_mode = True

datetime_strategy = DatetimeStrategy(test_mode=webserver_test_mode)

def get_datetime_strategy(request: Request) -> DatetimeStrategy:
    print(f'get_datetime_strategy(): returning the real datetime strategy')
    #return request.state.webserver
    return datetime_strategy

# TODO: this should not be in the limit_order_book_webserver module because
# it is used by everything that depends on datetime. Move to lib_datetime,
# if nothing else