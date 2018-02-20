from flask import Blueprint, request

from app.mod_main.models import Model, InvalidAPIKeyError

mod_api = Blueprint('api', __name__)

@mod_api.route('/api/add_garage')
def add_garage():
    return 'ok', 200

@mod_api.route('/api/add_report_event', methods=['POST'])
def add_report_event():
    api_key = request.headers.get('Authorization')

    try: 
        Model.add_report_event(api_key)
    except InvalidAPIKeyError:
        return 'not ok', 403
    
    return 'ok', 200