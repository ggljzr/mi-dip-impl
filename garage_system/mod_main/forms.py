from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import NumberRange


class UserSettingsForm(FlaskForm):
    notification_mail = StringField('Email pro upozornění')
    notifications = BooleanField('Povolit upozornění', default=True)


class GarageForm(FlaskForm):
    tag = StringField('Označení')
    period = IntegerField('Perioda hlášení (minuty)', validators=[NumberRange(
        1, 999, message='Perioda musí být mezi 1 a 999')])
    phone = StringField('Telefonní číslo')
    note = TextAreaField('Poznámka')


class GarageFormBuilder:

    def build_form(garage):
        garage_form = GarageForm()
        garage_form.tag.data = garage.tag
        garage_form.period.data = garage.period
        garage_form.note.data = garage.note
        garage_form.phone.data = garage.phone
        return garage_form
