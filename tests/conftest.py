import pytest

import testing_utils

@pytest.fixture(scope='module')
def app_client():
    # set app config to testing via env var
    testing_utils.setup()

    from garage_system.mod_auth.password_manager import PasswordManager
    pw_manager = PasswordManager()
    pw_manager.set_default_password()

    # initialize app with testing config
    # (garage module imports db from garage_system)
    from garage_system import db
    db.create_all() # reinitialize db scheme (because other tests might screw it up)

    from garage_system.mod_main.models.garage import Garage
    test_garage = Garage.add_garage()
    test_garage.api_key = 'testing_key' # we need to know garage api key
    db.session.commit() # commit new key

    from garage_system import app
    # set logged in flag to be true for all tests
    yield app.test_client()

    # teardown (delete db)
    testing_utils.teardown()