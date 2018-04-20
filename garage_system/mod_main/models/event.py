from garage_system import db
from .base import Base


class Event(Base):
    __tablename__ = 'event'

    TYPE_REPORT = 0
    TYPE_DOOR_OPEN = 1
    TYPE_DOOR_CLOSE = 2
    TYPE_MOVEMENT = 3
    TYPE_SMOKE = 4
    TYPE_DEVICE_ERROR = 5

    timestamp = db.Column(db.DateTime)

    garage_id = db.Column(db.Integer, db.ForeignKey(
        'garage.id'), nullable=False)
    type = db.Column(db.Integer, default=TYPE_REPORT)
