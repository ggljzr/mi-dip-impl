from flask_wtf import Form
from wtforms import StringField, IntegerField

class GarageForm(Form):
    tag = StringField('Označení')
    period = IntegerField('Perioda')