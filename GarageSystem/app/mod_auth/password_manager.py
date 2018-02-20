import bcrypt
import configparser

from config import USER_CONFIG_PATH

DEFAULT_PASSWORD = 'password'

class PasswordManager():

    def __init__(self):
        self.user_config = configparser.ConfigParser()
        self.user_config.read(USER_CONFIG_PATH)

    def check_password(self, password):
        pw_encoded = password.encode('utf-8')
        pw_hash = self.user_config['settings']['password'].encode('utf-8')

        return bcrypt.checkpw(pw_encoded, pw_hash)

    def check_default_password(self):
        return self.check_password(DEFAULT_PASSWORD)

    def save_password(self, new_password):
        pw_encoded = new_password.encode('utf-8')
        pw_hash = bcrypt.hashpw(pw_encoded, bcrypt.gensalt())
        self.user_config['settings']['password'] = pw_hash.decode('utf-8')

        with open(USER_CONFIG_PATH, 'w') as f:
            self.user_config.write(f)