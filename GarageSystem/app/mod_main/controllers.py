from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from jinja2 import Markup

from .models import Garage
from .forms import GarageFormBuilder, GarageForm

from app.mod_auth.auth_utils import login_required

mod_main = Blueprint('main', __name__)


@mod_main.app_template_filter('date_filter')
def date_filter(date):
    if date == None:
        return 'Žádné'

    return date

@mod_main.app_template_filter('garage_doors_filter')
def garage_doors_filter(doors):
    if doors == Garage.DOORS_OPEN:
        return 'Otevřeno'

    if doors == Garage.DOORS_CLOSED:
        return 'Zavřeno'

    return 'Nedefinováno'

@mod_main.app_template_filter('garage_state_filter')
def garage_state_filter(state):
    if state == Garage.STATE_OK:
        return 'OK'

    if state == Garage.STATE_NOT_RESPONDING:
        return 'Nehlásí se'

    return 'Nedefinováno'


@mod_main.route('/')
@login_required
def index():
    garages = Garage.query.all()
    return render_template('main/index.html', garages=garages)


@mod_main.route('/garage/<id>', methods=['GET'])
@login_required
def show_garage(id):
    garage = Garage.query.get(id)
    if garage == None:
        return render_template('404.html'), 404

    garage_form = GarageFormBuilder.build_form(garage)

    return render_template('main/show_garage.html', garage=garage, form=garage_form)


@mod_main.route('/garage/<id>', methods=['POST'])
@login_required
def edit_garage(id):
    garage = Garage.query.get(id)
    if garage == None:
        return render_template('404.html'), 404

    garage_form = GarageForm(request.form)
    if garage_form.validate_on_submit():
        garage.update(request.form.to_dict())
        flash('Garáž upravena')

    return render_template('main/show_garage.html', garage=garage, form=garage_form)


@mod_main.route('/revoke_key/<id>', methods=['POST'])
@login_required
def revoke_key(id):
    garage = Garage.query.get(id)
    if garage == None:
        return render_template('404.html'), 404

    garage.revoke_key()
    flash('Vygenerován nový klíč')
    return redirect('/garage/{}'.format(id))


@mod_main.route('/add_garage', methods=['POST'])
@login_required
def add_garage():
    Garage.add_garage()
    flash('Vytvořena nová garáž')
    return redirect('/')
