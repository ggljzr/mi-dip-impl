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

    events = db.relationship('Event', backref='Garage',
                             lazy=True, enable_typechecks=False)

    def __init__(self):
        self.api_key = uuid.uuid4().hex

class Event(Base):
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    garage_id = db.Column(db.Integer, db.ForeignKey(
        'garage.id'), nullable=False)


class ReportEvent(Event):
    next_report = db.Column(db.DateTime, default=None)
