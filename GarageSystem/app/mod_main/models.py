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
    api_key = db.Column(db.String(128), default='some_key')
    last_report = db.Column(db.DateTime, default=None)
    next_report = db.Column(db.DateTime, default=None)
    period = db.Column(db.Integer, default=60)
    state = db.Column(db.SmallInteger, default=0)

    def __init__(self):
        self.tag = 'New Garage'
        self.api_key = 'some_key' #nahodne generovany
        self.last_report = None
        self.next_report = None
        self.period = 60
        self.state = 0

    def __repr__(self):
        return 'Garage[{}]: {}'.format(self.id, self.tag)


class Model:
    def add_garage():
        new_garage = Garage()
        db.session.add(new_garage)
        db.session.commit()

    def get_all_garages():
        return Garage.query.all()

    def get_garage_by_id(id):
        return Garage.query.get(id)

    def update_garage(id, data):
        garage = Garage.query.get(id)
        garage.tag = data['tag']
        garage.period = data['period']
        db.session.commit()