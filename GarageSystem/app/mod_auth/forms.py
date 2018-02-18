from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import Length, EqualTo


class LoginForm(FlaskForm):
    password = PasswordField('Heslo')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Staré heslo')
    new_password = PasswordField('Nové heslo', validators=[
        Length(min=8, message='Heslo musí mít alespoň 8 znaků')])
    repeat_password = PasswordField('Nové heslo znovu', validators=[
        EqualTo('new_password', message='Hesla musí být stejná')])
