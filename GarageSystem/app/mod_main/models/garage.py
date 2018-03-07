from app import db
import uuid
from datetime import datetime, timedelta

from .base import Base
from .event import Event

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

class InvalidEventTypeError(Exception):
    pass

class Garage(Base):
    __tablename__ = 'garage'

    DOORS_OPEN = 0
    DOORS_CLOSED = 1

    STATE_OK = 0
    STATE_NOT_RESPONDING = 1
    STATE_SMOKE = 2
    STATE_MOVEMENT = 3

    REPORT_TOLERANCE = 60

    reg_mode = False

    tag = db.Column(db.String(64), default='Nová garáž')
    note = db.Column(db.String(256))
    api_key = db.Column(db.String(32), default=None)
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    doors = db.Column(db.SmallInteger, default=DOORS_OPEN)
    state = db.Column(db.SmallInteger, default=STATE_OK)

    events = db.relationship('Event', backref='Garage',
                             lazy=True, cascade='all, delete-orphan', order_by='desc(Event.timestamp)')

    def start_reg_mode():
        if Garage.reg_mode:
            return

        Garage.reg_mode = True

        def quit_req_mode():
            print('quitting')
            Garage.reg_mode = False

        quit_time = datetime.now() + timedelta(minutes=3)
        scheduler.add_job(quit_req_mode, run_date=quit_time)

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    #api_key uniquely identifies garage within database (same as id)
    #returns none when no matching garage is found
    def get_garage_by_key(api_key):
        garage = Garage.query.filter_by(api_key=api_key).first()
        return garage

    def check_reports():
        garages = Garage.query.all()
        for garage in garages:
            garage.check_report()

    def __init__(self):
        self.api_key = uuid.uuid4().hex

    #updates specific columns with corresponding dict
    def update(self, update_data):
        self.tag = update_data['tag']
        self.period = update_data['period']
        self.note = update_data['note']
        db.session.commit()

    def add_event(self, event_type):
        if event_type == Event.TYPE_REPORT:
            self.proc_report_event()
        elif event_type == Event.TYPE_DOOR_OPEN:
            self.proc_door_open_event()
        elif event_type == Event.TYPE_DOOR_CLOSED:
            self.proc_door_closed_event()
        elif event_type == Event.TYPE_MOVEMENT:
            self.proc_movement_event()
        elif event_type == Event.TYPE_SMOKE:
            self.proc_smoke_event()
        else:
            raise InvalidEventTypeError

        now = datetime.now()
        event = Event(garage_id=self.id, timestamp=now, type=event_type)
        self.events.append(event)
        db.session.commit()

    def proc_report_event(self):
        now = datetime.now()
        next_report = now + timedelta(minutes=self.period)

        self.last_report = now
        self.next_report = next_report

        if self.state == Garage.STATE_NOT_RESPONDING:
            self.state = Garage.STATE_OK

    def proc_door_open_event(self):
        pass

    def proc_door_closed_event(self):
        pass

    def proc_movement_event(self):
        pass

    def proc_smoke_event(self):
        pass

    def check_report(self):
        if self.next_report == None:
            return

        now = datetime.now()
        delta = now - self.next_report

        if delta.total_seconds() > Garage.REPORT_TOLERANCE:
            self.state = Garage.STATE_NOT_RESPONDING
            db.session.commit()

    #revokes garage api key by generating a new one
    def revoke_key(self):
        self.api_key = uuid.uuid4().hex
        db.session.commit()

    def delete_garage(self):
        db.session.delete(self)
        db.session.commit()
