from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from jinja2 import Markup

from .models.garage import Garage
from .forms import GarageFormBuilder, GarageForm, UserSettingsForm
from .filters import Filters

from garage_system.mod_auth.auth_utils import login_required

mod_main = Blueprint('main', __name__)


@mod_main.app_template_filter('date_filter')
def date_filter(date):
    return Filters.date_filter(date)


@mod_main.app_template_filter('garage_doors_filter')
def garage_doors_filter(doors):
    return Filters.garage_doors_filter(doors)


@mod_main.app_template_filter('garage_state_filter')
def garage_state_filter(state):
    return Filters.garage_state_filter(state)


@mod_main.app_template_filter('event_filter')
def event_filter(event):
    return Filters.event_filter(event)


@mod_main.app_template_filter('reg_mode_filter')
def reg_mode_filter(reg_mode):
    return Filters.reg_mode_filter(reg_mode)


@mod_main.route('/')
@login_required
def index():
    Garage.check_reports()
    garages = Garage.query.all()
    return render_template(
        'main/index.html', garages=garages, reg_mode=Garage.reg_mode)


@mod_main.route('/garage/<id>', methods=['GET'])
@login_required
def show_garage(id):
    garage = Garage.query.get(id)
    if garage is None:
        return render_template('404.html'), 404

    garage_form = GarageFormBuilder.build_form(garage)

    return render_template('main/show_garage.html',
                           garage=garage, form=garage_form)


@mod_main.route('/garage/<id>', methods=['POST'])
@login_required
def edit_garage(id):
    garage = Garage.query.get(id)
    if garage is None:
        return render_template('404.html'), 404

    garage_form = GarageForm(request.form)
    if garage_form.validate_on_submit():
        garage.update(request.form.to_dict())
        flash('Garáž upravena')

    return redirect('/garage/{}'.format(id))


@mod_main.route('/revoke_key/<id>', methods=['POST'])
@login_required
def revoke_key(id):
    garage = Garage.query.get(id)
    if garage is None:
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


@mod_main.route('/delete_garage/<id>', methods=['POST'])
@login_required
def delete_garage(id):
    garage = Garage.query.get(id)
    if garage is None:
        return render_template('404.html'), 404

    garage.delete_garage()

    flash('Garáž úspěšně smazáná')
    return redirect('/')


@mod_main.route('/reg_mode', methods=['POST'])
@login_required
def reg_mode():
    if Garage.reg_mode:
        flash('Registrační mód už běží', 'warning')
        return redirect('/')

    Garage.start_reg_mode()
    flash('Registrační mód spuštěn')
    return redirect('/')


@mod_main.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = UserSettingsForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        print(request.form.to_dict())
        flash('Nastavení uloženo')

    return render_template('main/user_settings.html', form=form)
