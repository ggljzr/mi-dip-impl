from flask import Blueprint, request

from app.mod_main.models.garage import Garage, InvalidEventTypeError

mod_api = Blueprint('api', __name__)

@mod_api.route('/api/garages', methods=['POST'])
def add_garage():
    if not Garage.reg_mode:
        return 'forbidden', 403

    Garage.add_garage()
    return 'created', 201

@mod_api.route('/api/events', methods=['POST'])
def add_report_event():
    api_key = request.headers.get('api_key')

    garage = Garage.get_garage_by_key(api_key)

    if garage == None:
        return 'forbidden', 403

    try:
        event_type = int(request.headers.get('event_type'))
        garage.add_event(event_type)
    except (InvalidEventTypeError, TypeError):
        return 'bad request', 400

    return 'created', 201