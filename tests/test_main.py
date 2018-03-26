import pytest
import os

"""
main controller unit tests

this also test application views (templates)
"""

@pytest.fixture(scope='module') # teardown after last test in module
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
    yield app.test_client()

    # teardown (delete db)
    testing_utils.teardown()