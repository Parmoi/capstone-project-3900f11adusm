import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, set_access_cookies
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

@APP.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    return auth.login(password, email=email)

@APP.route('/logout', methods=['POST'])
def logout():
    return auth.logout()

@APP.route('/register', methods=['POST'])
def register():
    email = request.json.get('email', None)
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    phone = request.json.get('phone', None)
    address = request.json.get('address', None)

    # TODO: Frontend can include first and last name fields in json if they want
    name = request.json.get('name', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)

    if name is not None:
        first_name = name
        last_name = ''

    return auth.register_collector(email, username, password, first_name=first_name, last_name=last_name, phone=phone, address=address)

@APP.route('/refresh', methods=['POST'])
@jwt_required(fresh=True)
def refresh_token():
    '''
    Refresh access token, makes user have to tokenticate credentials again
    '''
    user_id = get_jwt_identity()
    return auth.refresh(user_id)


@APP.route('/profile', methods=['GET'])
@jwt_required(fresh=False)
def profile():
    user_id = get_jwt_identity()
    return jsonify(dbm.get_collector(user_id)), 200

# TODO: Implement the wantlist function. Not sure how to select a users wantlist
#       Is the relational database set up so that each time a user is created, a wantlist
#       is instantiated. Or wantlist can be searched for and its contents retruned by
#       user id?
@APP.route('/wantlist', methods=['GET'])
@jwt_required(fresh=False)
def wantlist():
    user_id = get_jwt_identity()
    return jsonify(dbm.get_wantlist(user_id)), 200

@APP.route('/add')
def add_ran():
    dbm.insert_campaign("campaign 1", "random desc", "1999-01-01", "2000-01-01")
    dbm.insert_campaign("campaign 2", "random desc", "1999-01-01", "2001-01-01")
    dbm.insert_campaign("campaign 3", "random desc", "1999-01-01", "2025-01-01")
    dbm.insert_campaign("campaign 4", "random desc", "1999-01-01", "2030-01-01")
    dbm.insert_campaign("campaign 5", "random desc", "1999-01-01", "2023-10-19")
    dbm.insert_campaign("campaign 6", "random desc", "2024-10-19", "2030-10-19")
    dbm.insert_campaign("campaign 7", "random desc", "1999-01-01", "2023-10-20")
    return "add successful!", 200

@APP.route('/tester')
def tester():
    return jsonify(dbm.find_current_campaigns()), 200

# Example stubs for /dashboard and /collection
# @APP.route('/dashboard', methods=['GET'])
# @jwt_required(fresh=False)
# def dashboard():
#     user_id = get_jwt_identity()
#     return jsonify(dbm.get_dashboard(user_id)), 200

# @APP.route('/collection', methods=['GET'])
# @jwt_required(fresh=False)
# def collection():
#     user_id = get_jwt_identity()
#     return jsonify(dbm.get_collection(user_id)), 200



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


# Uncomment to have access token refreshed automatically after evert request is made
# If it is going to expire within a certain amount of time (optional)
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

if __name__ == "__main__":
    APP.run(host =config.host, port=config.port)
