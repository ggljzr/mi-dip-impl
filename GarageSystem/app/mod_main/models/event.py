from app import db
from .base import Base


class Event(Base):
    __tablename__ = 'event'

    TYPE_REPORT = 0
    TYPE_DOOR_OPEN = 1
    TYPE_DOOR_CLOSED = 2
    TYPE_MOVEMENT = 3
    TYPE_SMOKE = 4

    timestamp = db.Column(db.DateTime)

    garage_id = db.Column(db.Integer, db.ForeignKey(
        'garage.id'), nullable=False)
    type = db.Column(db.Integer, default=TYPE_REPORT)