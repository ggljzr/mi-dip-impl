import pytest
import os

import testing_config

@pytest.fixture()
def app():
    # set up -- load test config via var env
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'

    # create testing user config with default password
    from garage_system.mod_auth.password_manager import PasswordManager
    pw_manager = PasswordManager()
    pw_manager.set_default_password()

    # initialize and yield test application
    from garage_system import app
    yield app.test_client()

    # delete created user testing config
    os.unlink(testing_config.USER_CONFIG_PATH)
    try:
        os.unlink(BASE_DIR + '/test_app.db')
    except FileNotFoundError:
        pass

def test_login_required(app):
    response = app.get('/')

    # redirect to login page
    assert response.status == '302 FOUND'
    assert '/login' in response.headers['location']

# helper login function
def login_with_default_password(app):
    from garage_system.mod_auth.password_manager import DEFAULT_PASSWORD

    response = app.post('/login', data={
        'password' : DEFAULT_PASSWORD
        })

    return response

# helper logout function
def logout(app):
    response = app.get('/logout')
    return response

def test_invalid_password(app):
    response = app.post('/login', data={
        'password' : 'some fake password'
        })

    assert response.status == '403 FORBIDDEN'
    # flash error message is displayed
    assert 'Neplatné heslo' in response.data.decode('utf-8')

def test_default_password(app):
    # redirects to change password page
    response = login_with_default_password(app)

    assert response.status == '302 FOUND'
    assert '/change_password' in response.headers['location']

def test_password_change(app):
    from garage_system.mod_auth.password_manager import DEFAULT_PASSWORD

    new_password = 'some new password'

    # session is valid within test function
    login_with_default_password(app)

    # change password
    response = app.post('/change_password', data={
        'old_password' : DEFAULT_PASSWORD,
        'new_password' : new_password,
        'repeat_password' : new_password,
        'csrf_token' : 'fake token'
        })

    # check flash message
    assert 'flash_message' in response.data.decode('utf-8')

    # log out and try to log in with new password
    logout(app)
    
    response = app.post('/login', data={
        'password' : new_password
        })

    # we are redirected to homepage
    assert response.status == '302 FOUND'

# simple test if csrf protection is working
def test_csrf():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'

    from garage_system import app

    # turn on csrf protection
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_CHECK_DEFAULT'] = True

    # we can try csrf attack against login form
    # its basically post request without proper csrf token
    # (password value does not matter)
    response = app.test_client().post('/login', data={'password' : 'test password'})

    # we should get bad request status code
    # instead of expected forbidden (wrong password)
    assert response.status == '400 BAD REQUEST'

    # response should mention csrf
    assert 'CSRF' in response.data.decode('utf-8')