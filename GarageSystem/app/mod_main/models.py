from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

class Garage(Base):
    __tablename__ = 'garage'
    tag = db.Column(db.String(128), default='default garage')

    def __init__(self):
        self.tag = 'New Garage'

    def __repr__(self):
        return 'Garage[{}]: {}'.format(self.id, self.tag)

class Model:
    def __init__(self, app):
        pass

    def add_garage(self):
        pass

    def add_event(self, garage):
        pass

    def delete_garage(self):
        pass