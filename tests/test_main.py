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
    # we can see default garage tag
    assert 'Nová garáž' in response.data.decode('utf-8')

def test_garage_display(app_client, log_in_out):
    # get first garage
    response = app_client.get('/garage/1')

    assert response.status == '200 OK'
    assert 'show_garage_container' in response.data.decode('utf-8')
    # we can see default garage tag
    assert 'Nová garáž' in response.data.decode('utf-8')

def test_nonexistent_garage(app_client, log_in_out):
    response = app_client.get('/garage/468864684')

    # get 404
    assert response.status == '404 NOT FOUND'

def test_event_display(app_client, log_in_out):
    response = app_client.get('/garage/1')

    # we can see report event added in fixture
    assert 'Kontrolní hlášení' in response.data.decode('utf-8')

def test_edit_garage(app_client, log_in_out):
    # edit first garage data
    response = app_client.post('/garage/1', data={
        'tag' : 'some testing tag',
        'period' : 60,
        'note' : 'some testing note',
        'phone' : '+420732000111'
        }, follow_redirects=True) # follow redirect to updated page

    response_data = response.data.decode('utf-8')

    assert response.status == '200 OK'
    assert 'some testing tag' in response_data
    assert 'some testing note' in response_data
    assert '+420732000111' in response_data

def test_change_phone(app_client, log_in_out):
    test_phone = '+420732000111'

    response = app_client.post('/user_settings', data={
        'notification_phone' : test_phone
        }, follow_redirects=True) 
        # we follow redirect to settings page with our phone displayerd

    assert test_phone in response.data.decode('utf-8')

def test_fake_phone(app_client, log_in_out):
    test_phone = '0000'

    response = app_client.post('/user_settings', data={
        'notification_phone' : test_phone
        }, follow_redirects=True) 
        # we follow redirect to settings page with our phone displayerd

    assert response.status == '400 BAD REQUEST'