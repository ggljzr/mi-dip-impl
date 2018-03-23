import bcrypt
import configparser

from garage_system import app

DEFAULT_PASSWORD = 'password'


class PasswordManager():

    def __init__(self):
        self.user_config = configparser.ConfigParser()
        self.user_config.read(app.config['USER_CONFIG_PATH'])

    def check_password(self, password):
        pw_encoded = password.encode('utf-8')

        try:
            pw_hash = self.user_config['settings']['password'].encode('utf-8')
        except KeyError:
            pw_hash = bcrypt.hashpw(
                DEFAULT_PASSWORD.encode('utf-8'),
                bcrypt.gensalt())
            self.set_default_password()  # set default password if password section is missing

        return bcrypt.checkpw(pw_encoded, pw_hash)

    # checks if password in user_config.ini is default password
    def check_default_password(self):
        return self.check_password(DEFAULT_PASSWORD)

    def set_default_password(self):
        try:
            self.user_config.add_section('settings')
        except configparser.DuplicateSectionError:
            pass  # create settings section if it does not exists

        pw_hash = bcrypt.hashpw(
            DEFAULT_PASSWORD.encode('utf-8'),
            bcrypt.gensalt())
        self.user_config.set('settings', 'password', pw_hash.decode('utf-8'))

        with open(app.config['USER_CONFIG_PATH'], 'w') as f:
            self.user_config.write(f)

    def save_password(self, new_password):
        pw_encoded = new_password.encode('utf-8')
        pw_hash = bcrypt.hashpw(pw_encoded, bcrypt.gensalt())
        self.user_config['settings']['password'] = pw_hash.decode('utf-8')

        with open(app.config['USER_CONFIG_PATH'], 'w') as f:
            self.user_config.write(f)
