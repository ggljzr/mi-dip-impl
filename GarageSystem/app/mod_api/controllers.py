from flask import Blueprint

from app.mod_main.models import Model

mod_api = Blueprint('api', __name__)

@mod_api.route('/api/add_garage')
def add_garage():
    pass

@mod_api.route('/api/add_event', methods=['POST'])
def add_event():
    pass