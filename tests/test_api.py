import pytest

import testing_utils

"""
api controller unit tests

application model is tested separately
"""

def test_turned_off_regmode(app_client):
    response = app_client.post('/api/garages')
    assert response.status == '403 FORBIDDEN'

def test_fake_api_key(app_client):
    response = app_client.post('/api/report_event', headers={'api_key' : 'fake_key'})
    assert response.status == '403 FORBIDDEN'

def test_add_report_event(app_client):
    response = app_client.post('/api/report_event', headers={'api_key' : 'testing_key'})
    assert response.status == '201 CREATED'
    assert 'period' in response.data.decode('utf-8')

