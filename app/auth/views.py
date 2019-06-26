from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import Users

class RegistrationView(MethodView):
    # This class registers a new user.
    def post(self):
        # Handle POST request for this view. Url---> /auth/register

        # query to see if the user already exists
        user = user.query.filter_by(email=request.data['email']).first()
        if not user:
            # there is no user so we'll try to register them
            try:
                post_data = request.data
                #Register the user
                email = post_data['email']
                password = post_data['password']
                user = Users(email=email, password=password)
                user.save()

                response = {
                    'message': 'You have registered successfully. Please login.'
                    # return a response notify the user that they registered successful.
                }
                return make_response(jsonify(response)), 201
            
            except Exception as e:
                # an error occured, therefor return a string messege
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401

            else:
                # There is an existing user. We don't want to register user twice
                # Return a message  to the user telling the that they already exist
                response = {
                    'message': 'User already exists. Please login'
                }

                return make_response(jsonify(response)), 202
class LoginView(MethodView):
    # This class-based view handles user login and access token generation
    def post(self):
        # handle POST request for this view. url --> /auth/login
        try:
             # Get the user object using their email
            user = user.query.filter_by(email=request.data['email']).first()
            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
               # Generate the access token. This will be used as the authorization header
               access_token = user.generate_token(user.id)
               if access_token:
                   response = {
                       'message': 'You logged in successfully.',
                       'access_token': access_token.decode()
                   }
                   return make_response(jsonify(response)), 200
        else:
            # User does not exist. Therefor, we return an error
            response = {
                'message': 'Invalid email or password, Please try again'
            }
            return make_response(jsonify(response)), 401

        except Exception as e:
        # Create a response containing an string error message
            response = {
                'message': str(e)
                }
        # Return a server error using the HTTP Error code
            return make_response(jsonify(response)), 500

        # define the API resource
    login_view = LoginView.as_view('login-view')
    registration_view = RegistrationView.as_view('register_view')
    # Define the rule for registration url ---> /auth/register
    # Then add the rule to the blueprint
    auth_blueprint.add_url_rule(
        '/auth/register',
        view_func=registration_view,
        methods=['POST'])

    # Define the rule for the registration url ---> /auth/login
    # Then add the rule to the blueprint

    auth_blueprint.add_url_rule(
        '/auth/login',
        view_func=login_view
        methods=['POST'] )