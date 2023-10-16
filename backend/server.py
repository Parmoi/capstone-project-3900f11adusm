import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

import helpers.config as config
import helpers.exceptions as exceptions

from main import db_manager as dbm
from main import auth

APP = Flask(__name__)
APP.config.from_object(config.DevelopmentConfig)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, exceptions.defaultHandler)

CORS(APP)

# JWT App Settings
JWTManager(APP)
APP.config["JWT_COOKIE_SECURE"] = False
APP.config["JWT_TOKEN_LOCATION"] = ["cookies"]
APP.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
APP.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
APP.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
APP.config["JWT_COOKIE_CSRF_PROTECT"] = False

@APP.route('/')
def entry():
    return '<h1>Hello, Collector<h1\>'

@APP.route('/initdb')
def db_init():
    dbm.database_setup()
    return 'Database has been setup successfully!'

@APP.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = str(data["email"])
    password = str(data["password"])
    name = str(data["name"])

    return auth.register(email, password, name)

@APP.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    return auth.login(email, password)

@APP.route('/logout', methods=['POST'])
def logout():
    return auth.logout()


# @APP.after_request
# def refresh_expiring_jwts(response):
#     '''Refreshes users token if it is going to expire withing a given amount of time'''

#     exp_in = 60

#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=exp_in))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response

# @APP.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     '''
#     Example of protected route. Requires JWT to access.
#     Useful for when user has been logged in for a while and wants to edit profile.
#     '''

#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

# @APP.route("/protected_fresh", methods=["GET"])
# @jwt_required(fresh=True)
# def protected_fresh():
#     '''
#     Example of protected route. Requires fresh JWT to be fresh to access.
#     Useful for when user has been logged in for a while and wants to edit profile.
#     '''

#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

# @APP.route('/refresh', methods=['POST'])
# @jwt_required(fresh=True)
# def refresh_token():
#     '''
#     Refresh access token, makes user have to tokenticate credentials again
#     '''

#     # Create the new access token
#     user = get_jwt_identity()
#     access_token = create_access_token(identity=user)

#     # Retruns a non fresh access token
#     response = jsonify({'refresh': True})
#     set_access_cookies(response, access_token)
#     return response, 200


if __name__ == "__main__":
    APP.run(host =config.host, port=config.port)
