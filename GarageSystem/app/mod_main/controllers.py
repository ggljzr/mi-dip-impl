from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from jinja2 import Markup

from .models import Model
from .forms import GarageFormBuilder, GarageForm

mod_main = Blueprint('main', __name__)

@mod_main.app_template_filter('garage_display')
def garage_display(garage):
    gid = garage.id
    string = '<a href="/garage/{}">Garáž[{}]: {}<a/><br>'.format(
        gid, gid, garage.tag)
    return Markup(string)


@mod_main.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return redirect('/login')

    garages = Model.get_all_garages()
    return render_template('main/index.html', garages=garages)


@mod_main.route('/garage/<id>', methods=['GET', 'POST'])
def show_garage(id):
    if not session.get('logged_in'):
        return redirect('/')

    garage = Model.get_garage_by_id(id)
    if garage == None:
        return render_template('404.html')

    garage_form = GarageFormBuilder.build_form(garage)

    if request.method == 'POST':
        # kdyz se postuje novej formular
        # tak chci vzit ten z toho postu
        # a ne ten vygenerovanej builderem z ty
        # puvodni garaze
        garage_form = GarageForm(request.form)
        if garage_form.validate_on_submit():
            Model.update_garage(id, request.form.to_dict())
            flash('Garáž upravena')

    return render_template('main/garage_view.html', garage=garage, form=garage_form)


@mod_main.route('/create_garage', methods=['GET'])
def create_garage():
    if not session.get('logged_in'):
        return redirect('/')

    Model.add_garage()
    return redirect('/')
