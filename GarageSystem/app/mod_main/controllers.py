from flask import Blueprint, render_template, request, redirect, url_for

from jinja2 import Markup

from app.mod_main.models import Model
from app.mod_main.forms import GarageForm

mod_main = Blueprint('main', __name__)

#na ten filtr se asi spis vysrat nebo ho nak
#poupravit aby se pres nej neformatovala cela garaz
@mod_main.app_template_filter('garage_display')
def garage_display(garage):
    gid = garage.id
    string = '<a href="/garage/{}">Garage[{}]: {}<a/><br>'.format(gid, gid, garage.tag)
    return Markup(string)

@mod_main.route('/', methods=['GET'])
def index():
    garages = Model.get_all_garages()
    return render_template('main/index.html', garages=garages)

@mod_main.route('/garage/<id>')
def show_garage(id):
    garage = Model.get_garage_by_id(id)
    if garage == None:
        return render_template('404.html')

    garage_form = GarageForm()

    return render_template('main/garage_view.html', garage=garage, form=garage_form)

#vytvoreni garaze v uzivatelskym rozhrani
@mod_main.route('/create_garage', methods=['GET'])
def create_garage():
    Model.add_garage()
    return redirect(url_for('main.index'))

@mod_main.route('/edit_garage/<id>', methods=['POST'])
def edit_garage(id):
    Model.update_garage(id, request.form)
    return redirect('/')
