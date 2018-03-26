import pytest
import os

import testing_config
import testing_utils

"""
api controller unit tests

application model is tested separately
"""

@pytest.fixture(scope='module')
def app():
    # set up -- load test config via var env
    testing_utils.setup()

    from garage_system import db
    db.create_all() # reinitialize db scheme (because other tests might screw it up)

    from garage_system.mod_main.models.garage import Garage
    test_garage = Garage.add_garage()
    test_garage.api_key = 'testing_key' # we need to know garage api key

    # initialize and yield test application
    from garage_system import app
    db.session.commit() # commit new key
    yield app.test_client()

    # teardown
    testing_utils.teardown()

def test_turned_off_regmode(app):
    response = app.post('/api/garages')
    assert response.status == '403 FORBIDDEN'

def test_fake_api_key(app):
    response = app.post('/api/report_event', headers={'api_key' : 'fake_key'})
    assert response.status == '403 FORBIDDEN'

def test_add_report_event(app):
    response = app.post('/api/report_event', headers={'api_key' : 'testing_key'})
    assert response.status == '201 CREATED'
    assert 'period' in response.data.decode('utf-8')

