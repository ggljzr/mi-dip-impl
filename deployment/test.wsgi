import sys
import os
sys.path.insert(0, '/var/www/test')
from test import app as application
application.secret_key = os.urandom(12)
