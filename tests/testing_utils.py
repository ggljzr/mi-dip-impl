import os

from testing_config import BASE_DIR, USER_CONFIG_PATH

# load test config via var env
def setup():
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'
    try:
        os.unlink(BASE_DIR + '/test_app.db') # delete current test db
    except FileNotFoundError:
        pass

# delete test_app.db and user config created for testing
def teardown():
    try:
        os.unlink(USER_CONFIG_PATH)
    except FileNotFoundError:
        pass

    try:
        os.unlink(BASE_DIR + '/test_app.db')
    except FileNotFoundError:
        pass