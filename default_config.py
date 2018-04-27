DEBUG = True

import os
# this means app.db, user_config.ini are created in the same
# directory as this file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO=True
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

SECRET_KEY = os.urandom(16)
# set session lifetime to 6 hours
# after that user is logged out automatically
PERMANENT_SESSION_LIFETIME = 6 * 60 * 60 # seconds

USER_CONFIG_PATH = os.path.join(BASE_DIR, 'user_config.ini')
