from passlib.hash import argon2
import configparser

DEFAULT_PASSWORD = 'password'

"""
Class for managing user_config.ini. 
Allows checking and updating password and phone number.
"""
class ConfigManager():

    def __init__(self, config_path):
        self.config_path = config_path
        self.reload_config()

    def write_config(self):
        with open(self.config_path, 'w') as f:
            self.user_config.write(f)

    def check_password(self, password):
        try:
            pw_hash = self.user_config['settings']['password']
        except KeyError:
            # hash function from passlib autogenerates 
            # salt for each password, see https://passlib.readthedocs.io/en/stable/lib/passlib.hash.argon2.html
            pw_hash = argon2.hash(DEFAULT_PASSWORD)
            self.set_default_password()  # set default password if password section is missing

        return argon2.verify(password, pw_hash)

    # checks if password in user_config.ini is default password
    # this could be refactored if needed so we dont need to calculate
    # hash every time we check for default password 
    # (mantain self.default_password flag or something)
    # but this seems fast enough and slightly more readable
    def check_default_password(self):
        return self.check_password(DEFAULT_PASSWORD)

    def set_default_password(self):
        self.save_password(DEFAULT_PASSWORD)

    def save_password(self, new_password):
        pw_hash = argon2.hash(new_password)
        self.user_config['settings']['password'] = pw_hash
        self.write_config()

    def save_phone(self, phone):
        self.user_config['settings']['phone'] = phone
        self.write_config()

    def read_phone(self):
        phone = None
        try:
            phone = self.user_config['settings']['phone']
        except KeyError:
            pass
        return phone # return None when no phone is filled out

    """
    Method to reload given config file. File is created if it
    does not exists. In the same way section 'settings' is created.

    Method can be used when config file is changed outside config manager.
    """
    def reload_config(self):
        self.user_config = configparser.ConfigParser()
        self.user_config.read(self.config_path)

        try:
            self.user_config.add_section('settings')
        except configparser.DuplicateSectionError:
            pass  # create settings section if it does not exists

        self.write_config()