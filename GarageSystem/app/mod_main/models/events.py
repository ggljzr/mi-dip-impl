from app import db
from .base import Base


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


class SmokeEvent(Event):
    __tablename__ = 'smokeevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'smokeevent'
    }

    def __repr__(self):
        return super(DoorOpenEvent, self).__repr__() + ' Detekce kouře!'


class MovementEvent(Event):
    __tablename__ = 'movementevent'

    id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'movementevent'
    }

    def __repr__(self):
        return super(DoorOpenEvent, self).__repr__() + ' Detekce pohybu!'
