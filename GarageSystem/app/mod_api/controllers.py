from flask import Blueprint, request

from app.mod_main.models import Garage

mod_api = Blueprint('api', __name__)

@mod_api.route('/api/add_garage')
def add_garage():
    return 'ok', 200

@mod_api.route('/api/add_report_event', methods=['POST'])
def add_report_event():
    api_key = request.headers.get('api_key')

    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return 'not ok', 403
    
    garage.add_report_event()

    return 'ok', 200