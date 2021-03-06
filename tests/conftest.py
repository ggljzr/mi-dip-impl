import pytest

import testing_utils

@pytest.fixture(scope='module')
def app_client():
    # set app config to testing via env var
    testing_utils.setup()

    from garage_system import config_manager
    config_manager.set_default_password()

    # initialize app with testing config
    # (garage module imports db from garage_system)
    from garage_system import db
    db.create_all() # reinitialize db scheme (because other tests might screw it up)

    from garage_system.mod_main.models.garage import Garage
    test_garage = Garage.add_garage()
    test_garage.api_key = 'testing_key' # we need to know garage api key
    db.session.commit() # commit new key

    # add some event we can check
    # make sure we get more than one page of events
    from garage_system.mod_main.controllers import PAGE_SIZE
    for i in range(0, PAGE_SIZE * 2):
        if i % 2 == 0:
            test_garage.add_smoke_event()
        else:
            test_garage.add_report_event()

    # to make sure garage is in ok state
    test_garage.add_report_event()

    from garage_system import app
    # set logged in flag to be true for all tests
    yield app.test_client()

    # teardown (delete db)
    testing_utils.teardown()
    # load empty config
    config_manager.reload_config()

# fixture to set and clear logged_in flag
# in flask session
@pytest.fixture()
def log_in_out(app_client):
    testing_utils.set_logged_in(app_client, True)
    yield None
    testing_utils.set_logged_in(app_client, False)