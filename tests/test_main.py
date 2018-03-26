import pytest

import testing_utils
from flask import session

"""
main controller unit tests

this also test application views (templates)
"""

@pytest.fixture() # teardown after last test in module
def app_client():
    # set app config to testing via env var
    testing_utils.setup()

    # initialize app with testing config
    # (garage module imports db from garage_system)
    from garage_system import db
    db.create_all() # reinitialize db scheme (because other tests might screw it up)

    from garage_system.mod_main.models.garage import Garage
    test_garage = Garage.add_garage()

    from garage_system import app
    # set logged in flag to be true for all tests
    yield app.test_client()

    # teardown (delete db)
    testing_utils.teardown()

def test_index(app_client):
    testing_utils.set_logged_in(app_client)
    response = app_client.get('/')
    # we get main page right away
    # (no redirects)
    assert response.status == '200 OK'
    assert 'garages_box' in response.data.decode('utf-8')

def test_garage(app_client):
    testing_utils.set_logged_in(app_client)

    # get first garage
    response = app_client.get('/garage/1')

    assert response.status == '200 OK'
    assert 'show_garage_container' in response.data.decode('utf-8')

def test_nonexistent_garage(app_client):
    testing_utils.set_logged_in(app_client)

    response = app_client.get('/garage/468864684')

    # get 404
    assert response.status == '404 NOT FOUND'

def test_edit_garage(app_client):
    testing_utils.set_logged_in(app_client)

    # edit first garage data
    response = app_client.post('/garage/1', data={
        'tag' : 'some testing tag',
        'period' : 60,
        'note' : 'some testing note'
        }, follow_redirects=True) # follow redirect to updated page

    response_data = response.data.decode('utf-8')

    assert response.status == '200 OK'
    assert 'some testing tag' in response_data
    assert 'some testing note' in response_data


