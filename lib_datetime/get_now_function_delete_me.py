

# import os


# NOTE: This environment variable should NOT be set by Unit Test Code.
# It is here so that systems can switch the Webserver mode into a test mode
# so that the webserver can be deployed to UAT systems for testing.
# webserver_test_mode = False
# if os.environ.get('ENABLE_WEBSERVER_TEST_MODE'):
#     webserver_test_mode = True

# if webserver_test_mode:
#     now = now_fake # TODO: what is `now` ??? module.now?
# else:
#     now = now_real
# TODO: how to incorporate an environment variable with the boolean from __init__?
# TODO: reenable?


