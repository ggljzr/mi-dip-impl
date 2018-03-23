import pytest
import os

@pytest.fixture(scope='module')
def app():
    # set up -- load test config via var env
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'

    # initialize and yield test application
    from garage_system import app
    yield app.test_client()

def test_login_required(app):
    response = app.get('/')

    # redirect to login page
    assert response.status == '302 FOUND'
    assert 'login' in response.headers['location']