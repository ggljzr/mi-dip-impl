from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import NumberRange


class GarageForm(FlaskForm):
    tag = StringField('Označení')
    period = IntegerField('Perioda', validators=[NumberRange(
        1, 999, message="Perioda musí být mezi 1 a 999")])
    note = TextAreaField('Poznámka')


class GarageFormBuilder:

    def build_form(garage):
        garage_form = GarageForm()
        garage_form.tag.data = garage.tag
        garage_form.period.data = garage.period
        garage_form.note.data = garage.note
        return garage_form
