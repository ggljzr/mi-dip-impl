from flask_wtf import FlaskForm
from wtforms import PasswordField

class LoginForm(FlaskForm):
    password = PasswordField('Heslo')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Staré heslo')
    new_password = PasswordField('Nové heslo')
    repeat_password = PasswordField('Nové heslo znovu')