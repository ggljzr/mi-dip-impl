import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
# test tips : http://alexmic.net/flask-sqlalchemy-pytest/
#           : http://flask.pocoo.org/docs/0.12/testing/#testing
#           : https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code (yield thing)

import testing_utils

"""
model (garage and event) unit tests
"""

@pytest.fixture(scope='module') # teardown after last test in module
def garage():
    # set app config to testing via env var
    testing_utils.setup()

    # initialize app with testing config
    # (garage module imports db from garage_system)
    from garage_system import db
    db.create_all() # reinitialize db scheme (because other tests might screw it up)

    from garage_system.mod_main.models.garage import Garage
    yield Garage

    # teardown (delete db)
    testing_utils.teardown()

def test_add_garage(garage):
    garage.add_garage()
    # adds exactly one garage
    assert len(garage.query.all()) == 1

def test_revoke_key(garage):
    new_garage = garage.add_garage()
    old_key = new_garage.api_key
    new_garage.revoke_key()

    assert old_key != new_garage.api_key

# freeze time so we always have the same now
@freeze_time("2011-01-01 00:00:00")
def test_add_report(garage):
    new_garage = garage.add_garage()
    new_garage.add_report_event()
    now = datetime.now()
    next = now + timedelta(minutes=new_garage.period)

    assert new_garage.last_report == now
    assert new_garage.next_report == next
    assert new_garage.state == garage.STATE_OK
    assert len(new_garage.events) == 1

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

def test_smoke_event(garage):
    new_garage = garage.add_garage()
    new_garage.add_smoke_event()
    assert new_garage.state == garage.STATE_SMOKE

def test_movemenent_doors_open(garage):
    new_garage = garage.add_garage()
    new_garage.add_door_open_event() # open doors

    # now we should not register movement events
    # so garage state should not change after adding one
    # this apply only for movement event
    new_garage.add_movement_event()

    assert new_garage.state == garage.STATE_OK
    # added event signalize subsystem error
    from garage_system.mod_main.models.event import Event
    assert new_garage.events[0].type == Event.TYPE_DEVICE_ERROR

def test_movement_event(garage):
    new_garage = garage.add_garage()

    # close garage doors so we register movement events
    new_garage.add_door_close_event()

    new_garage.add_movement_event()
    assert new_garage.state == garage.STATE_MOVEMENT

    # garage does not change state after smoke event
    # as per specification
    new_garage.state = garage.STATE_SMOKE
    new_garage.add_movement_event()
    assert new_garage.state == garage.STATE_SMOKE

def test_open_close(garage):
    new_garage = garage.add_garage()

    new_garage.add_door_open_event()
    assert new_garage.doors == garage.DOORS_OPEN

    new_garage.add_door_close_event()
    assert new_garage.doors == garage.DOORS_CLOSE

def test_delete_garage(garage):
    old_garage_num = len(garage.query.all())
    new_garage = garage.add_garage()
    new_garage.delete_garage()

    assert old_garage_num == len(garage.query.all())

def test_get_events(garage):
    new_garage = garage.add_garage()
    new_garage.add_report_event()
    new_garage.add_report_event()
    new_garage.add_smoke_event()

    from garage_system.mod_main.models.event import Event

    assert len(new_garage.get_events()) == 3
    assert len(new_garage.get_events(Event.TYPE_REPORT)) == 2
    assert len(new_garage.get_events(Event.TYPE_SMOKE)) == 1 