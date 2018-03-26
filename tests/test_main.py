import pytest

import testing_utils
from flask import session

"""
main controller unit tests

this also test application views (templates)
"""


def test_index(app_client, log_in_out):
    response = app_client.get('/')
    # we get main page right away
    # (no redirects)
    assert response.status == '200 OK'
    assert 'garages_box' in response.data.decode('utf-8')
    # we can see garage tag
    assert 'Nová garáž' in response.data.decode('utf-8')

def test_garage(app_client, log_in_out):
    # get first garage
    response = app_client.get('/garage/1')

    assert response.status == '200 OK'
    assert 'show_garage_container' in response.data.decode('utf-8')
    # we can see garage tag
    assert 'Nová garáž' in response.data.decode('utf-8')

def test_nonexistent_garage(app_client, log_in_out):
    response = app_client.get('/garage/468864684')

    # get 404
    assert response.status == '404 NOT FOUND'

def test_edit_garage(app_client, log_in_out):
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


