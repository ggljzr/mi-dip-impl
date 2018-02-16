from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import NumberRange

class GarageForm(FlaskForm):
    tag = StringField('Označení')
    period = IntegerField('Perioda', validators=[NumberRange(1, 999, message="Perioda musí být mezi 1 a 999")])