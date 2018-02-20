from app import db
import uuid

from .models import Garage, ReportEvent


class InvalidAPIKeyError(Exception):
    pass


class ModelFacade:

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    def get_all_garages():
        return Garage.query.all()

    def get_garage_by_id(id):
        return Garage.query.get(id)

    def get_garage_by_key(api_key):
        garage = Garage.query.filter_by(api_key=api_key).first()

        if garage == None:
            raise InvalidAPIKeyError

        return garage

    def update_garage(id, update_data):
        garage = Garage.query.get(id)
        garage.tag = update_data['tag']
        garage.period = update_data['period']
        db.session.commit()

    def revoke_key(id):
        garage = Garage.query.get(id)

        if garage != None:
            garage.api_key = uuid.uuid4().hex
            db.session.commit()

    def add_report_event(api_key):
        garage = ModelFacade.get_garage_by_key(api_key)

        event = ReportEvent(garage_id=garage.id)
        garage.events.append(event)
        db.session.commit()
