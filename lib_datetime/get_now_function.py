
from fastapi import Request

from lib_datetime.real_datetime import now as now_real
from lib_datetime.fake_datetime import now as now_fake

import os


# NOTE: This environment variable should NOT be set by Unit Test Code.
# It is here so that systems can switch the Webserver mode into a test mode
# so that the webserver can be deployed to UAT systems for testing.
webserver_test_mode = False
if os.environ.get('ENABLE_WEBSERVER_TEST_MODE'):
    webserver_test_mode = True

if webserver_test_mode:
    now = now_fake
else:
    now = now_real


datetime_implementation_is_fake = False

def get_now_function():
    print('get_now_function returning the REAL now function')
    print(f'now={now}')
    print(now())
    #return request.state.webserver
    return now
