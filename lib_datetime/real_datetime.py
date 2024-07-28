
from lib_datetime import fake_datetime

from datetime import datetime
from datetime import timezone

import os


# NOTE: This environment variable should NOT be set by Unit Test Code.
# It is here so that systems can switch the Webserver mode into a test mode
# so that the webserver can be deployed to UAT systems for testing.
#
# The environment variable is here to override the behaviour of now() to
# provide a known value for testing purposes in UAT environments.

if os.environ.get('ENABLE_WEBSERVER_TEST_MODE'):
    webserver_test_mode = True
else:
    webserver_test_mode = False


def now() -> datetime:
    if webserver_test_mode:
        return fake_datetime.now()
    else:
        return datetime.now(timezone.utc)
