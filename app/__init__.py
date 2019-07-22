from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response
from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Parcels, Users
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/parcels/', methods=['POST', 'GET'])
    def parcels():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Attempt to decode the token and get the user id
            user_id = Users.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authorized

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
       
                    if name:
                        parcel = Parcels(name=name)
                        parcel.save()
                        response = jsonify({
                            'id': parcel.id,
                            'parcel_name': parcel.parcel_name,
                            'date_created': parcel.date_created,
                            'date_modified': parcel.date_modified,
                            'pickup_destination': parcel.pickup_destination,
                            'delivery_destination': parcel.delivery_destination,
                            'parcel_number': parcel.parcel_number,
                            'created_by': user_id
                        })
                
                return make_response(response), 201

            else:
                #GET att the parcels created by this user
                parcels = Parcels.query.filter_by(created_by=user_id)
                results = []

                for parcel in parcels:
                    obj = {
                        'id':parcel.id,
                        'parcel_name':parcel.parcel_name,
                        'date_created':parcel.date_created,
                        'date_modified':parcel.date_modified,
                        'pickup_destination':parcel.pickup_destination,
                        'delivery_destination':parcel.delivery_destination,
                        'parcel_number':parcel.parcel_number,
                        'created_by': parcel.created_by
                    }

                    results.append(obj)
            
                return  make_response(jsonify(results)), 200

        else:
            message = user_id
            response = {
                'message': message
            }  
            return make_response(jsonify(response)), 401

    @app.route('/parcels/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def parcel_manipulation(id, **kwargs):
         # get the access token from the authorization header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        
        if access_token:
            # Get the user id related to this access token
            user_id = Users.decode_token(access_token) 
        
            if not isinstance(user_id, str):
                parcel = Parcels.query.filter_by(id=id).first()

                if not parcel:
                #Raise an HTTPException with 404 not staging
                    abort(404)

                if request.method == 'DELETE':
                    parcel.delete()
                    return {
                        "message": "parcel {} deleted successfully".format(parcel.id)
                    }, 200

            elif request.method == 'PUT':
                name = str(request.data.get('name', ''))
                parcel.name = name
                parcel.save()
                response = jsonify({
                    'id':parcel.id,
                    'parcel_name':parcel.parcel_name,
                    'date_created':parcel.date_created,
                    'date_modified':parcel.date_modified,
                    'pickup_destination':parcel.pickup_destination,
                    'delivery_destination':parcel.delivery_destination,
                    'parcel_number':parcel.parcel_number,
                    'created_by': parcel.created_by
                })
                return make_response(jsonify(response)), 200
            
            else:
            # GET
                response = {
                    'id':parcel.id,
                    'parcel_name':parcel.parcel_name,
                    'date_created':parcel.date_created,
                    'date_modified':parcel.date_modified,
                    'pickup_destination':parcel.pickup_destination,
                    'delivery_destination':parcel.delivery_destination,
                    'parcel_number':parcel.parcel_number,
                    'created_by': parcel.created_by
                }
           
            return make_response(jsonify(response)), 200

        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            # return an error response, telling the user he is Unauthorized
            return make_response(jsonify(response)), 401
        # import the authentication blueprint and register it on the app
    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app
