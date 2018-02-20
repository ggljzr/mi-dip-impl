from app import db
import uuid

from .models import Garage, ReportEvent


class InvalidAPIKeyError(Exception):
    pass

class InvalidGarageIDError(Exception):
    pass

class ModelFacade:

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    def get_all_garages():
        return Garage.query.all()

    def get_garage_by_id(id):
        garage = Garage.query.get(id)

        if garage == None:
            raise InvalidGarageIDError

        return garage

    def get_garage_by_key(api_key):
        garage = Garage.query.filter_by(api_key=api_key).first()

        if garage == None:
            raise InvalidAPIKeyError

        return garage

    def update_garage(garage, update_data):
        garage.tag = update_data['tag']
        garage.period = update_data['period']
        db.session.commit()

    def revoke_key(id):
        try:
            garage = ModelFacade.get_garage_by_id(id)
        except InvalidGarageIDError:
            return

        garage.api_key = uuid.uuid4().hex
        db.session.commit()

    def add_report_event(garage):
        event = ReportEvent(garage_id=garage.id)
        garage.events.append(event)
        db.session.commit()
