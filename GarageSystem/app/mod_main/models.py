from app import db
import uuid
from datetime import datetime, timedelta


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class Garage(Base):
    __tablename__ = 'garage'

    STATE_OPEN = 0
    STATE_CLOSED = 1
    STATE_NOT_RESPODING = 2

    tag = db.Column(db.String(64), default='Nová garáž')
    note = db.Column(db.String(256))
    api_key = db.Column(db.String(32), default=None)
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    state = db.Column(db.SmallInteger, default=STATE_OPEN) #tady pouzit nakej enum jestli je 

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
    def add_report_event(self):
        now = datetime.now()
        next_report = now + timedelta(minutes=self.period)

        event = ReportEvent(garage_id=self.id, timestamp=now,
                            next_report=next_report)
        self.events.append(event)
        self.last_report = now
        self.next_report = next_report
        db.session.commit()

        return self.period

    #checks if garage missed its expected report
    def check_report(self):
        pass

    #revokes garage api key by generating a new one
    def revoke_key(self):
        self.api_key = uuid.uuid4().hex
        db.session.commit()

    def __repr__(self):
        return '[{}] {} Poslední hlášení: {}'.format(self.id, self.tag, self.last_report)


class Event(Base):
    __tablename__ = 'event'

    timestamp = db.Column(db.DateTime)

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

class DoorOpenEvent(Event):
    __tablename__ = 'dooropenevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'dooropenevent'
    }

    def __repr__(self):
        return super(DoorOpenEvent, self).__repr__() + ' Otevření dveří'

class DoorClosedEvent(Event):
    __tablename__ = 'doorclosedevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'doorclosedevent'
    }

    def __repr__(self):
        return super(DoorOpenEvent, self).__repr__() + ' Zavření dveří'

class SmokeDetectorEvent(Event):
    __tablename__ = 'smokedetectorevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'smokedetectorevent'
    }

    def __repr__(self):
        return super(DoorOpenEvent, self).__repr__() + ' Detekce kouře!'

class MovementDetectorEvent(Event):
    __tablename__ = 'movementdetectorevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'movementdetectorevent'
    }

    def __repr__(self):
        return super(DoorOpenEvent, self).__repr__() + ' Detekce pohybu!'