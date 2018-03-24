import pytest
import os

import testing_config

@pytest.fixture()
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
    """
    from garage_system.mod_auth.password_manager import DEFAULT_PASSWORD
    from garage_system.mod_auth.forms import ChangePasswordForm

    new_password = 'some new password'

    # session is valid within test function
    login_with_default_password(app)

    # change password
    response = app.post('/change_password', data={
        'old_password' : DEFAULT_PASSWORD,
        'new_password' : new_password,
        'repeat_password' : new_password
        })

    # log out and try to log in with new password
    logout(app)

    print(response.data.decode('utf-8'))
    
    response = app.post('/login', data={
        'password' : new_password
        })

    assert response.status == '302 FOUND'
    """

    pass
