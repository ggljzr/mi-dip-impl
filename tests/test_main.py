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
    assert 'Kontrolní hlášení</td>' in response.data.decode('utf-8')

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

def test_edit_garage_bad_request(app_client, log_in_out):
    response = app_client.post('/garage/1', data={
        'tag' : 'some testing tag',
        'period' : -60,
        'note' : 'some testing note',
        'phone' : 'some fake phone'
        }, follow_redirects=True) # follow redirect to updated page

    assert response.status == '400 BAD REQUEST'

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

def test_paging(app_client, log_in_out):
    response = app_client.get('/garage/1')
    data = response.data.decode('utf-8')

    # we can see page links
    assert '&gt;0&lt;' in data # page zero is selected
    assert '[1]' in data

    # we can flip to other page
    response = app_client.get('/garage/1?index=1')
    data = response.data.decode('utf-8')

    assert response.status == '200 OK'
    assert 'Kontrolní hlášení</td>' in data

def test_filtering(app_client, log_in_out):
    # get all events
    response = app_client.get('/garage/1')
    data = response.data.decode('utf-8')

    # we see report events and smoke events
    assert 'Kontrolní hlášení</td>' in data
    assert 'Detekce kouře!</td>' in data

    # get only report events
    response = app_client.get('/garage/1?event_type=0')
    data = response.data.decode('utf-8')

    assert 'Kontrolní hlášení</td>' in data
    assert 'Detekce kouře!</td>' not in data

    # get only smoke events
    response = app_client.get('/garage/1?event_type=4')
    data = response.data.decode('utf-8')

    assert 'Kontrolní hlášení</td>' not in data
    assert 'Detekce kouře!</td>' in data
