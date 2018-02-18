import bcrypt
import configparser

from config import USER_CONFIG_PATH

class PasswordManager():
    def __init__(self):
        self.user_config = configparser.ConfigParser()
        self.user_config.read(USER_CONFIG_PATH)

    def check_password(self, password):
        if password == self.user_config['settings']['password']:
            return True

        return False

    def save_password(self, password):
        pass