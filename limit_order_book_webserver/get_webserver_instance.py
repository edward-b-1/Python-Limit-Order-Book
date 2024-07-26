
from fastapi import Request

from lib_webserver.webserver import Webserver

import os


# NOTE: This environment variable should NOT be set by Unit Test Code.
# It is here so that systems can switch the Webserver mode into a test mode
# so that the webserver can be deployed to UAT systems for testing.
webserver_test_mode = False
if os.environ.get('ENABLE_WEBSERVER_TEST_MODE'):
    webserver_test_mode = True

webserver = Webserver(use_fake_webserver=webserver_test_mode)

def get_webserver_instance(request: Request) -> Webserver:
    #return request.state.webserver
    return webserver
