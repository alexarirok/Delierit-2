#app/models.py
from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
class Users(db.Model):
    # This class represents the Users table
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    parcels = db.relationship(
        'Parcels', order_by='Parcels.id', cascade="all, delete-orphan")


    def __init__(self, email, password):
        # initialize with name.
        self.name = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        # Checks the password against it's hash to validates
        return Bcrypt().check_password_hash(self.password, password)


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def generate_token(self, user_id):
        #generate the access token

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            #creates the byte string token using the payload and secrete key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algarithm = 'HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
     # DEcodes the access token from the Authorization header
        try:
             # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"
    
class Parcels(db.Model):
    __tablename__ = "parcels"

    id = db.Column(db.Integer, primary_key=True)
    parcel_name = db.Column(db.String(255))
    pickup_destination = db.Column(db.String(255))
    delivery_destination = db.Column(db.String(255))
    parcel_number = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
    db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, name, created_by):
        # initialize with name.
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        #This method gets all the parcels for a given user.
        return Parcels.query.filter_by(created_by=user_id)

    def delete(self):
        # Deletes a given bucketlist
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        # Return a representation of a parcel instance
        return "<Users: {}>".format(self.name)
