from flask import Blueprint
# this instance of a blueprint that represents the authentication
auth_blueprint = Blueprint('auth', __name__)

from . import views

def create_app(config_name):

    @app.route('/parcels/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def parcel_manipulation(id, **kwargs):

       # import the authentication blueprint and register it
    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint) 

    return app