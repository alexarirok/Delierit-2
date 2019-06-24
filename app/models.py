#app/models.py
from app import db

class Users(db.Model):
    # This class represents the Users table
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        # initialize with name.
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Users.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Users: {}>".format(self.name)

class Parcels(db.Model):
    __tablename__ = "parcels"

    id = db.Column(db.Integer, primary_key=True)
    parcel_name = db.column(db.String(255))
    pickup_destination = db.column(db.String(255))
    delivery_destination = db.column(db.String(255))
    parcel_number = db.column(db.Integer())
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
    db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    def __init__(self, name):
        # initialize with name.
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Parcels.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Users: {}>".format(self.name)
