DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_SECRET_KEY = os.urandom(16)
SECRET_KEY = os.urandom(16)

USER_CONFIG_PATH = os.path.join(BASE_DIR, 'user_config.ini')