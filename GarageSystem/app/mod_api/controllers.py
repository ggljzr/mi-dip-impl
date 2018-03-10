from flask import Blueprint, request
import json

from app.mod_main.models.garage import Garage, InvalidEventTypeError

mod_api = Blueprint('api', __name__)

@mod_api.route('/api/garages', methods=['POST'])
def add_garage():
    if not Garage.reg_mode:
        ret = {'status' : 403}
        return json.dumps(ret), 403

    new_garage = Garage.add_garage()
    ret = {'status' : 201, 'key' : new_garage.api_key}
    return json.dumps(ret), 201

@mod_api.route('/api/events', methods=['POST'])
def add_report_event():
    api_key = request.headers.get('api_key')

    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        ret = {'status' : 403}
        return json.dumps(ret), 403

    try:
        event_type = int(request.headers.get('event_type'))
        garage.add_event(event_type)
    except (InvalidEventTypeError, TypeError):
        ret = {'status' : 400}
        return json.dumps(ret), 400


    ret = {'status' : 201, 'next_report' : garage.period}
    return json.dumps(ret), 201