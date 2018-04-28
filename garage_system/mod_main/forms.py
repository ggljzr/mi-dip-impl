from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, ValidationError
from wtforms.validators import NumberRange

from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException

"""
Validator for phone number used in user settings and garage form.
"""
def validate_phone_number(form, field):
    if field.data is '':
        return

    error_message = 'Neplatné telefonní číslo'

    try:
        phone = parse(field.data)
    except NumberParseException:
        raise ValidationError(error_message)
    else:
        if not is_valid_number(phone):
            raise ValidationError(error_message)


class UserSettingsForm(FlaskForm):
    notification_phone = StringField(
        'Telefon pro upozornění (včetně předvolby)', validators=[validate_phone_number])


class GarageForm(FlaskForm):
    tag = StringField('Označení')
    period = IntegerField('Perioda hlášení (minuty)', validators=[NumberRange(
        1, 999, message='Perioda musí být mezi 1 a 999')])
    phone = StringField('Telefonní číslo', validators=[validate_phone_number])
    note = TextAreaField('Poznámka')

"""
Class to build GarageForm from given garage class instance.
"""
class GarageFormBuilder:

    def build_form(garage):
        garage_form = GarageForm()
        garage_form.tag.data = garage.tag
        garage_form.period.data = garage.period
        garage_form.note.data = garage.note
        garage_form.phone.data = garage.phone
        return garage_form
