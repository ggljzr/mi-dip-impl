from flask import Blueprint, request
import json

from garage_system.mod_main.models.garage import Garage

mod_api = Blueprint('api', __name__)

def wrap_status_code(code):
    ret = {'status' : code}
    return json.dumps(ret), code


@mod_api.route('/api/garages', methods=['POST'])
def add_garage():
    if not Garage.reg_mode:
        return wrap_status_code(403)

    new_garage = Garage.add_garage()
    ret = {'status' : 201, 'api_key' : new_garage.api_key}
    return json.dumps(ret), 201

@mod_api.route('/api/report_event', methods=['POST'])
def add_report_event():
    api_key = request.headers.get('api_key')
    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return wrap_status_code(403)

    garage.add_report_event()

    ret = {'status' : 201, 'period' : garage.period}
    return json.dumps(ret), 201

@mod_api.route('/api/door_open_event', methods=['POST'])
def add_door_open_event():
    api_key = request.headers.get('api_key')
    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return wrap_status_code(403)

    garage.add_door_open_event()

    return wrap_status_code(201)

@mod_api.route('/api/door_close_event', methods=['POST'])
def add_door_closed_event():
    api_key = request.headers.get('api_key')
    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return wrap_status_code(403)

    garage.add_door_close_event()

    return wrap_status_code(201)

@mod_api.route('/api/movement_event', methods=['POST'])
def add_movement_event():
    api_key = request.headers.get('api_key')
    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return wrap_status_code(403)

    garage.add_movement_event()

    return wrap_status_code(201)

@mod_api.route('/api/smoke_event', methods=['POST'])
def add_smoke_event():
    api_key = request.headers.get('api_key')
    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return wrap_status_code(403)

    garage.add_smoke_event()

    return wrap_status_code(201)