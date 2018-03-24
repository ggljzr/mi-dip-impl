import pytest
import os

import testing_config

@pytest.fixture(scope='module')
def app():
    # set up -- load test config via var env
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'
    try:
        os.unlink(testing_config.USER_CONFIG_PATH) # delete current testing user config
    except FileNotFoundError:
        pass

    # create testing user config with default password
    from garage_system.mod_auth.password_manager import PasswordManager
    pw_manager = PasswordManager()
    pw_manager.set_default_password()

    # initialize and yield test application
    from garage_system import app
    yield app.test_client()

    # delete created user testing config
    os.unlink(testing_config.USER_CONFIG_PATH)

def test_login_required(app):
    response = app.get('/')

    # redirect to login page
    assert response.status == '302 FOUND'
    assert 'login' in response.headers['location']

def test_default_password(app):
    from garage_system.mod_auth.password_manager import DEFAULT_PASSWORD

    response = app.post('/login', data={
        'password' : DEFAULT_PASSWORD
        })

    # redirects to change password page
    assert response.status == '302 FOUND'
    assert 'change_password' in response.headers['location']

def test_invalid_password(app):
    response = app.post('/login', data={
        'password' : 'some fake password'
        }, follow_redirects=True) # follow redirect so we can check flash message

    # redirects to /login with flashed error message
    assert response.status == '200 OK'
    # check if flash_error css class tag is in returned data
    assert 'flash_error' in response.data.decode('utf-8')

def test_password_change(app):
    pass