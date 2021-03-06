from garage_system import db, scheduler
import uuid
from datetime import datetime, timedelta

from .base import Base
from .event import Event

"""
Garage class represents garage subsystem
and implements event logging logic.
"""
class Garage(Base):
    __tablename__ = 'garage'

    DOORS_OPEN = 0
    DOORS_CLOSE = 1

    STATE_OK = 0
    STATE_NOT_RESPONDING = 1
    STATE_SMOKE = 2
    STATE_MOVEMENT = 3

    REPORT_TOLERANCE = 60 # see check_report() method

    REG_MODE_TIMER = 3 # see start_reg_mode() method

    reg_mode = False

    tag = db.Column(db.String(64), default='Nová garáž')
    note = db.Column(db.String(256))
    api_key = db.Column(db.String(32), default=None)
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    doors = db.Column(db.SmallInteger, default=DOORS_OPEN)
    state = db.Column(db.SmallInteger, default=STATE_OK)
    phone = db.Column(db.String(64))

    # because event collection can be somewhat large
    # we use dynamic lazy loading
    # this speeds up adding new events
    # for more info see http://docs.sqlalchemy.org/en/latest/orm/collections.html
    events = db.relationship('Event', backref='Garage',
                             lazy='dynamic', cascade='all, delete-orphan', order_by='desc(Event.timestamp)')

    """
    Method to start reg mode. Method sets reg_mode flag to True and schedules
    job to to set it to false after REG_MODE_TIMER minutes.
    """
    def start_reg_mode():
        if Garage.reg_mode:
            return

        Garage.reg_mode = True

        def quit_req_mode():
            Garage.reg_mode = False

        quit_time = datetime.now() + timedelta(minutes=Garage.REG_MODE_TIMER)
        scheduler.add_job(quit_req_mode, run_date=quit_time, id='reg_job')

    """
    Method that sets reg_mode flag to false and removes eventual scheduled quit.
    """
    def quit_reg_mode():
        scheduler.remove_job('reg_job')
        Garage.reg_mode = False

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()
        return new_garage

    """
    Api_key uniquely identifies garage within database (same as id).
    Returns none when no matching garage is found.
    """
    def get_garage_by_key(api_key):
        garage = Garage.query.filter_by(api_key=api_key).first()
        return garage

    """
    See check_report().
    """
    def check_reports():
        garages = Garage.query.all()
        for garage in garages:
            garage.check_report()

    def __init__(self):
        self.api_key = uuid.uuid4().hex

    """
    Updates specific columns with corresponding dict.
    """
    def update(self, update_data):
        self.tag = update_data['tag']
        self.period = update_data['period']
        self.note = update_data['note']
        self.phone = update_data['phone']
        db.session.commit()

    """
    Method used internaly by other add_ methods.
    """
    def add_event(self, type):
        now = datetime.now()
        event = Event(garage_id=self.id, timestamp=now, type=type)
        self.events.append(event)
        db.session.commit()

    """
    Methods for adding events. Each event has its own method,
    so we dont need to check valid event type.
    """
    def add_report_event(self):
        now = datetime.now()
        next_report = now + timedelta(minutes=self.period)

        self.last_report = now
        self.next_report = next_report

        self.state = Garage.STATE_OK

        self.add_event(Event.TYPE_REPORT)

    def add_door_open_event(self):
        self.doors = Garage.DOORS_OPEN
        self.add_event(Event.TYPE_DOOR_OPEN)

    def add_door_close_event(self):
        self.doors = Garage.DOORS_CLOSE
        self.add_event(Event.TYPE_DOOR_CLOSE)

    def add_movement_event(self):
        # door are opened so we should not
        # recieve any movement events from
        # deactivated subsystem, 
        # meaning something strange is happening
        if self.doors == Garage.DOORS_OPEN:
            # add event siganlizing subsystem error
            self.add_event(Event.TYPE_DEVICE_ERROR)
            return

        if self.state == Garage.STATE_OK:
            self.state = Garage.STATE_MOVEMENT

        self.add_event(Event.TYPE_MOVEMENT)

    def add_smoke_event(self):
        if self.state == Garage.STATE_OK or self.state == Garage.STATE_MOVEMENT:
            self.state = Garage.STATE_SMOKE

        self.add_event(Event.TYPE_SMOKE)

    """
    Wraper for SQLAlchemy Query object that is events.
    Returns events with specified type or all events if
    event_type == None.

    Returns None if no events with given type exists in
    the database (default SQLAlchemy query behavior). 
    """
    def get_events(self, event_type=None):
        if event_type is None:
            return self.events.all()

        return self.events \
        .filter(Event.type == event_type) \
        .all()

    """
    Checks if subsystem (garage) is past due with its report
    (if its past next_report time + REPORT_TOLERANCE).

    If report was missed, sets garage state to NOT_RESPONDING.

    Returns True if report was not missed yet, False otherwise.
    """
    def check_report(self):
        if self.next_report is None:
            return True

        now = datetime.now()
        delta = now - self.next_report

        if delta.total_seconds() > Garage.REPORT_TOLERANCE:
            self.state = Garage.STATE_NOT_RESPONDING
            db.session.commit()
            return False

        return True

    """
    Revokes garage api key by generating a new one.
    """
    def revoke_key(self):
        self.api_key = uuid.uuid4().hex
        db.session.commit()

    def delete_garage(self):
        db.session.delete(self)
        db.session.commit()
