from app import db
import uuid


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class Garage(Base):
    __tablename__ = 'garage'

    tag = db.Column(db.String(64), default='Nová garáž')
    note = db.Column(db.String(256))
    api_key = db.Column(db.String(32), default=None)
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    state = db.Column(db.SmallInteger, default=0)

    events = db.relationship('Event', backref='Garage',
                             lazy=True)

    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    def get_garage_by_key(api_key):
        garage = Garage.query.filter_by(api_key=api_key).first()
        return garage

    def __init__(self):
        self.api_key = uuid.uuid4().hex

    def update(self, update_data):
        self.tag = update_data['tag']
        self.period = update_data['period']
        self.note = update_data['note']
        db.session.commit()

    def add_report_event(self):
        event = ReportEvent(garage_id=self.id)
        self.events.append(event)
        db.session.commit()

    def revoke_key(self):
        self.api_key = uuid.uuid4().hex
        db.session.commit()

class Event(Base):
    __tablename__ = 'event'

    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    garage_id = db.Column(db.Integer, db.ForeignKey(
        'garage.id'), nullable=False)
    type = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'event',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '[{}]'.format(self.timestamp)


class ReportEvent(Event):
    __tablename__ = 'reportevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    next_report = db.Column(db.DateTime, default=None)

    __mapper_args__ = {
        'polymorphic_identity': 'reportevent'
    }

    def __repr__(self):
        return super(ReportEvent, self).__repr__() + ' Kontrolní hlášení'