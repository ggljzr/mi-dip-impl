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