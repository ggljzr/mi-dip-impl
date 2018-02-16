from flask import Blueprint, render_template, request, redirect, url_for

from jinja2 import Markup

from app.mod_main.models import Model

mod_main = Blueprint('main', __name__)

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

    return render_template('main/garage_view.html', garage=garage)

#vytvoreni garaze v uzivatelskym rozhrani
@mod_main.route('/create_garage', methods=['GET'])
def create_garage():
    Model.add_garage()
    return redirect(url_for('main.index'))

#editace tagu pres form v garage_view
@mod_main.route('/set_garage_tag/<id>', methods=['POST'])
def set_garage_tag(id):
    new_tag = request.form['tag']
    Model.set_garage_tag(id, new_tag)
    return redirect('/garage/{}'.format(id))
