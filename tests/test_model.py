import pytest
import os

# test tips : http://alexmic.net/flask-sqlalchemy-pytest/
#           : http://flask.pocoo.org/docs/0.12/testing/#testing

import testing_config

@pytest.fixture
def garage():
    # set app config to testing via env var
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['GARAGE_SYSTEM_CONFIG'] = BASE_DIR + '/testing_config.py'

    # initialize app with testing config
    from garage_system.mod_main.models.garage import Garage
    yield Garage

    # teardown (delete db)
    os.unlink(BASE_DIR + '/test_app.db')

def test_add_garage(garage):
    garage.add_garage()
    # adds exactly one garage
    assert len(garage.query.all()) == 0