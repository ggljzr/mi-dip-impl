from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from jinja2 import Markup

from .models import Model
from .forms import GarageFormBuilder, GarageForm

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')

    garages = Model.get_all_garages()
    return render_template('main/index.html', garages=garages)


@mod_main.route('/garage/<id>', methods=['GET', 'POST'])
def show_garage(id):
    if not session.get('logged_in'):
        return redirect('/login')

    garage = Model.get_garage_by_id(id)
    if garage == None:
        return render_template('404.html'), 404

    garage_form = GarageFormBuilder.build_form(garage)

    if request.method == 'POST':
        #load form from user when they submitting new settings
        garage_form = GarageForm(request.form)
        if garage_form.validate_on_submit():
            Model.update_garage(id, request.form.to_dict())
            flash('Garáž upravena')

    return render_template('main/show_garage.html', garage=garage, form=garage_form)


@mod_main.route('/create_garage', methods=['GET'])
def create_garage():
    if not session.get('logged_in'):
        return redirect('/login')

    Model.add_garage()
    flash('Vytvořena nová garáž')
    return redirect('/')
