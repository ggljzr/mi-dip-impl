from app import db

import uuid


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class Garage(Base):
    tag = db.Column(db.String(128), default='Nová garáž')
    api_key = db.Column(db.String(32), default=None)
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    state = db.Column(db.SmallInteger, default=0)

    events = db.relationship('Event', backref='Garage', lazy=True, enable_typechecks=False)

    def __init__(self):
        self.api_key = uuid.uuid4().hex

    def __repr__(self):
        return 'Garáž[{}]: {}'.format(self.id, self.tag)


class Event(Base):
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    garage_id = db.Column(db.Integer, db.ForeignKey(
        'garage.id'), nullable=False)

class ReportEvent(Event):
    next_report = db.Column(db.DateTime, default=None)

class InvalidAPIKeyError(Exception):
    pass

class Model:

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    def get_all_garages():
        return Garage.query.all()

    def get_garage_by_id(id):
        return Garage.query.get(id)

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
        garage = Garage.query.filter_by(api_key=api_key).first()

        if garage == None:
            raise InvalidAPIKeyError
        else:
            event = ReportEvent(garage_id=garage.id)
            garage.events.append(event)
            db.session.commit()
