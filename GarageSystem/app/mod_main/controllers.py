from flask import Blueprint, render_template, request, redirect, url_for

#mozna to udelat tak ze ten model nebude
#v zadnym modulu a pak budu mit moduly jako
#api nebo main_page ktery ho budou pouzivat
from app.mod_main.models import Model

mod_main = Blueprint('main', __name__)

@mod_main.route('/', methods=['GET'])
def index():
    garages = Model.get_all_garages()
    return render_template('main/index.html', garages=garages)

#vytvoreni garaze v uzivatelskym rozhrani
@mod_main.route('/create_garage', methods=['GET'])
def create_garage():
    #tady pro vytvareni novejch instanci a tak
    #asi pouzit fasadu v modelu
    Model.add_garage()
    return redirect(url_for('main.index'))
