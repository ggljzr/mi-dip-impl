from app import db
import uuid
from datetime import datetime, timedelta

from .base import Base
from .events import ReportEvent

class Garage(Base):
    __tablename__ = 'garage'

    DOORS_OPEN = 0
    DOORS_CLOSED = 1

    STATE_OK = 0
    STATE_NOT_RESPONDING = 1
    STATE_SMOKE = 2
    STATE_MOVEMENT = 3

    tag = db.Column(db.String(64), default='Nová garáž')
    note = db.Column(db.String(256))
    api_key = db.Column(db.String(32), default=None)
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    doors = db.Column(db.SmallInteger, default=DOORS_OPEN)
    state = db.Column(db.SmallInteger, default=STATE_OK)

    events = db.relationship('Event', backref='Garage',
                             lazy=True)

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    #api_key uniquely identifies garage within database (same as id)
    #returns none when no matching garage is found
    def get_garage_by_key(api_key):
        garage = Garage.query.filter_by(api_key=api_key).first()
        return garage

    def __init__(self):
        self.api_key = uuid.uuid4().hex

    #updates specific columns with corresponding dict
    def update(self, update_data):
        self.tag = update_data['tag']
        self.period = update_data['period']
        self.note = update_data['note']
        db.session.commit()

    # returns minutes to the next expected report
    # also sets state to OK if it was NOT_RESPONDING
    def add_report_event(self):
        now = datetime.now()
        next_report = now + timedelta(minutes=self.period)

        event = ReportEvent(garage_id=self.id, timestamp=now,
                            next_report=next_report)
        self.events.append(event)
        self.last_report = now
        self.next_report = next_report

        if self.state == Garage.STATE_NOT_RESPONDING:
            self.state = Garage.STATE_OK

        db.session.commit()

        return self.period

    def add_door_open_event(self):
        pass

    def add_door_closed_event(self):
        pass

    def add_movement_event(self):
        pass

    def add_smoke_event(self):
        pass

    #checks if garage missed its expected report
    #also sets state to NOT_RESPONDING if report was missed
    def check_report(self):
        pass

    #revokes garage api key by generating a new one
    def revoke_key(self):
        self.api_key = uuid.uuid4().hex
        db.session.commit()

    def __repr__(self):
        return '[{}] {} Poslední hlášení: {}'.format(self.id, self.tag, self.last_report)

