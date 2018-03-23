import pytest
import os
from datetime import datetime, timedelta
from freezegun import freeze_time
# test tips : http://alexmic.net/flask-sqlalchemy-pytest/
#           : http://flask.pocoo.org/docs/0.12/testing/#testing
#           : https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code (yield thing)

import testing_config

@pytest.fixture(scope='module') # teardown after last test in module
def garage():
    # set app config to testing via env var
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'

    # initialize app with testing config
    # (garage module imports db from garage_system)
    from garage_system.mod_main.models.garage import Garage
    yield Garage

    # teardown (delete db)
    os.unlink(BASE_DIR + '/test_app.db')

def test_add_garage(garage):
    garage.add_garage()
    # adds exactly one garage
    assert len(garage.query.all()) == 1

def test_revoke_key(garage):
    new_garage = garage.add_garage()
    old_key = new_garage.api_key
    new_garage.revoke_key()

    assert old_key != new_garage.api_key

@freeze_time("2011-01-01 00:00:00")
def test_add_report(garage):
    new_garage = garage.add_garage()
    new_garage.add_report_event()
    now = datetime.now()
    next = now + timedelta(minutes=new_garage.period)

    assert new_garage.last_report == now
    assert new_garage.next_report == next
    assert new_garage.state == garage.STATE_OK

@freeze_time("2011-01-01 00:00:00")
def test_check_report(garage):
    new_garage = garage.add_garage()
    new_garage.period = 60 # explicitly set period
    new_garage.add_report_event()
    new_garage.check_report()

    assert new_garage.state == garage.STATE_OK

    # move time forward two hours so report is missed
    with freeze_time("2011-01-01 02:00:00"):
        new_garage.check_report()
        assert new_garage.state == garage.STATE_NOT_RESPONDING
