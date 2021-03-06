import pytest

import testing_utils

"""
auth controller unit tests

(including password manager functionality)
"""

def test_login_get(app_client):
    response = app_client.get('/login')

    # login form is displayed
    assert 'login_box' in response.data.decode('utf-8')

def test_login_required(app_client):
    response = app_client.get('/')

    # redirect to login page
    assert response.status == '302 FOUND'
    assert '/login' in response.headers['location']

def test_invalid_password(app_client):
    response = app_client.post('/login', data={
        'password' : 'some fake password'
        })

    assert response.status == '403 FORBIDDEN'
    # flash error message is displayed
    assert 'flash_error' in response.data.decode('utf-8')
    assert 'Neplatné heslo' in response.data.decode('utf-8')

def test_default_password(app_client):
    # redirects to change password page
    response = testing_utils.login_with_default_password(app_client)

    assert response.status == '302 FOUND'
    assert '/change_password' in response.headers['location']

def test_logout(app_client, log_in_out):
    response = app_client.post('/logout', follow_redirects=True)

    # redirects to /login
    assert response.status == '200 OK'
    # message about logging out is displayed
    assert 'flash_message' in response.data.decode('utf-8')
    assert 'Odhlášení proběhlo úspěšně' in response.data.decode('utf-8')

    # cant access app after logout
    response = app_client.get('/') # redirects to /login
    assert response.status == '302 FOUND'
    assert '/login' in response.headers['location']


def test_password_change(app_client, log_in_out):
    from garage_system.mod_auth.config_manager import DEFAULT_PASSWORD

    new_password = 'some new password'

    # change password
    response = app_client.post('/change_password', data={
        'old_password' : DEFAULT_PASSWORD,
        'new_password' : new_password,
        'repeat_password' : new_password,
        }, follow_redirects=True)

    # check flash message
    assert response.status == '200 OK'
    assert 'flash_message' in response.data.decode('utf-8')
    assert 'změněno' in response.data.decode('utf-8')

    # log out and try to log in with new password
    testing_utils.set_logged_in(app_client, False)
    
    response = app_client.post('/login', data={
        'password' : new_password
        }, follow_redirects=True)

    # we are redirected to homepage
    # instead of getting 403
    assert response.status == '200 OK'
    # we can see garages now
    assert 'garages_box' in response.data.decode('utf-8')

# simple test if csrf protection is working
def test_csrf():
    testing_utils.setup()

    from garage_system import app

    # turn on csrf protection
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_CHECK_DEFAULT'] = True

    # we can try csrf attack against login form
    # its basically post request without proper csrf token
    # (password value does not matter)
    response = app.test_client().post('/login', data={
        'password' : 'test password',
        'csrf_token' : 'some fake token'
        })

    # we should get bad request status code
    # instead of expected forbidden (wrong password)
    assert response.status == '400 BAD REQUEST'

    # response should mention csrf
    assert 'CSRF' in response.data.decode('utf-8')

    testing_utils.teardown()

    # turn csrf protection off again for other tests
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False