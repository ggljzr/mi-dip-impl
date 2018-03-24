DEBUG = True
TESTING = True

import os
# this means app.db, user_config.ini are created in the same
# directory as this file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test_app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

# csrf disabled for testing
WTF_CSRF_ENABLED = False

# interesting sidenote: if this would be set to false
# in production, every from would have to be validated
# via validate() method, to force checking csrf token
WTF_CSRF_CHECK_DEFAULT = False

SECRET_KEY = 'testing key'

USER_CONFIG_PATH = os.path.join(BASE_DIR, 'test_user_config.ini')