from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Parcels
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/parcels/', methods=['POST', 'GET'])
    def parcels():
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
                })
                response.status_code = 201
                return response

            else:
                #GET
                parcels = Parcels.get_all()
                result = []

                for parcel in parcels:
                    obj = {
                        'id':parcel.id,
                        'parcel_name':parcel.parcel_name,
                        'date_created':parcel.date_created,
                        'date_modified':parcel.date_modified,
                        'pickup_destination':parcel.pickup_destination,
                        'delivery_destination':parcel.delivery_destination,
                        'parcel_number':parcel.parcel_number,
                    }

                    result.append(obj)
                response = jsonify(result)
                response.status_code = 200
                return response
    
    @app.route('/parcels/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def parcel_manipulation(id, **kwargs):
        # retrive a parcel using its ID
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
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id':parcel.id,
                'parcel_name':parcel.parcel_name,
                'date_created':parcel.date_created,
                'date_modified':parcel.date_modified,
                'pickup_destination':parcel.pickup_destination,
                'delivery_destination':parcel.delivery_destination,
                'parcel_number':parcel.parcel_number,
            })
            response.status_code = 200
            return response

    return app
