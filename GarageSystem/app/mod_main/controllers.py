from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from jinja2 import Markup

from .model_facade import ModelFacade, InvalidGarageIDError
from .forms import GarageFormBuilder, GarageForm

from app.mod_auth.auth_utils import login_required

mod_main = Blueprint('main', __name__)

@mod_main.app_template_filter('date_filter')
def date_filter(date):
    if date == None:
        return 'Žádné'

    return date

@mod_main.route('/')
@login_required
def index():
    garages = ModelFacade.get_all_garages()
    return render_template('main/index.html', garages=garages)


@mod_main.route('/garage/<id>', methods=['GET', 'POST'])
@login_required
def show_garage(id):
    try:
        garage = ModelFacade.get_garage_by_id(id)
    except InvalidGarageIDError:
        return render_template('404.html'), 404

    garage_form = GarageFormBuilder.build_form(garage)

    if request.method == 'POST':
        #load form from user when they submitting new settings
        garage_form = GarageForm(request.form)
        if garage_form.validate_on_submit():
            ModelFacade.update_garage(garage, request.form.to_dict())
            flash('Garáž upravena')

    return render_template('main/show_garage.html', garage=garage, form=garage_form)


@mod_main.route('/revoke_key/<id>')
@login_required
def revoke_key(id):
    ModelFacade.revoke_key(id)
    flash('Vygenerován nový klíč')
    return redirect('/garage/{}'.format(id))

@mod_main.route('/add_garage')
@login_required
def add_garage():
    ModelFacade.add_garage()
    flash('Vytvořena nová garáž')
    return redirect('/')
