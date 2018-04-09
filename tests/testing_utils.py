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


# helper login function
def login_with_default_password(app_client):
    from garage_system.mod_auth.config_manager import DEFAULT_PASSWORD

    response = app_client.post('/login', data={
        'password' : DEFAULT_PASSWORD
        })

    return response

# helper logout function
def logout(app_client):
    response = app_client.post('/logout')
    return response

# sets logged in flag in flask session
# bypases auth controller, password check
# (unlike login/logout functions)
def set_logged_in(app_client, value):
    with app_client as c:
        with c.session_transaction() as s:
            s['logged_in'] = value
