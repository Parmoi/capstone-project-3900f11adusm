import os
import json
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
)

from flask_cors import CORS
from datetime import timedelta

import helpers.config as config
import helpers.exceptions as exceptions

from main.database import db_manager as dbm
from main.database import (
    db_collectors,
    db_campaigns,
    db_waintlist,
    db_collectibles,
    db_collections,
)
from main import auth
from main.error import InputError, AccessError, OK
from mock_data import mock_data_init

APP = Flask(__name__)
APP.config.from_object(config.DevelopmentConfig)
APP.config["TRAP_HTTP_EXCEPTIONS"] = True
APP.register_error_handler(Exception, exceptions.defaultHandler)

CORS(APP, supports_credentials=True)

# JWT App Settings
JWTManager(APP)
APP.config["JWT_COOKIE_SECURE"] = False
APP.config["JWT_TOKEN_LOCATION"] = ["cookies"]
APP.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
APP.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
APP.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
APP.config["JWT_COOKIE_CSRF_PROTECT"] = False


@APP.route("/")
def entry():
    return "<h1>Hello, Collector<h1\>"


""" |------------------------------------|
    |          Database Routes           |
    |------------------------------------| """


@APP.route("/initdb")
def db_init():
    dbm.database_setup()
    return jsonify(msg="Database has been setup successfully!"), OK


@APP.route("/init_mock_data", methods=["GET"])
def init_mock_data():
    mock_data_init.execute_sql_file("./mock_data/mock_collectors.sql")
    db_campaigns.register_campaign(
        "mock",
        "Mock collectibles campaign!",
        "2023-10-23",
        "2023-10-23",
        ["rarity", "condition", "color"],
    )
    mock_data_init.execute_sql_file("./mock_data/mock_collectibles.sql")

    return jsonify(msg="Mock data initialised!"), OK


""" |------------------------------------|
    |       Authentication Routes        |
    |------------------------------------| """


@APP.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    return auth.login(password, email=email)


@APP.route("/logout", methods=["POST"])
def logout():
    return auth.logout()


@APP.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    return auth.register_collector(
        email,
        username,
        password,
    )


@APP.route("/refresh", methods=["POST"])
@jwt_required(fresh=True)
def refresh_token():
    """
    Refresh access token, makes user have to tokenticate credentials again
    """
    user_id = get_jwt_identity()
    return auth.refresh(user_id)

# @APP.route("/add")
# def add_random():
#     db_campaigns.register_campaign("campaign 1", "random desc", "1999-01-01", "2000-01-01", [])
#     db_campaigns.register_campaign("campaign 2", "random desc", "1999-01-01", "2001-01-01", [])
#     db_campaigns.register_campaign("campaign 3", "random desc", "1999-01-01", "2025-01-01", [])
#     db_campaigns.register_campaign("campaign 4", "random desc", "1999-01-01", "2030-01-01", [])
#     db_campaigns.register_campaign("campaign 5", "random desc", "1999-01-01", "2023-10-19", [])
#     db_campaigns.register_campaign("campaign 6", "random desc", "2024-10-19", "2030-10-19", [])
#     db_campaigns.register_campaign("campaign 7", "random desc", "1999-01-01", "2023-10-20", [])
#     return "add successful"

# @APP.route("/search1")
# def first_search():
#     return db_campaigns.find

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

""" |------------------------------------|
    |          Collector Routes          |
    |------------------------------------| """


@APP.route("/profile", methods=["GET"])
@jwt_required(fresh=False)
def profile():
    user_id = get_jwt_identity()
    return db_collectors.get_collector(user_id)


@APP.route("/profile/update", methods=["POST"])
@jwt_required(fresh=False)
def profile_update():
    user_id = get_jwt_identity()

    email = request.json.get("email", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    phone = request.json.get("phone", None)
    address = request.json.get("address", None)

    return db_collectors.update_collector(
        id=user_id,
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        password=password,
        address=address,
    )


@APP.route("/get_collectors", methods=["GET"])
def get_collectors():
    return db_collectors.get_all_collectors()


""" |------------------------------------|
    |           Campaign Routes          |
    |------------------------------------| """


@APP.route("/campaign/register", methods=["POST"])
# @jwt_required(fresh=False)
def register_campaign():
    # verify_jwt_in_request()

    name = request.json.get("name", None)
    description = request.json.get("desc", None)
    start_date = request.json.get("start", None)
    end_date = request.json.get("end", None)
    collectible_fields = request.json.get("fields", None)

    return db_campaigns.register_campaign(
        name, description, start_date, end_date, collectible_fields
    )


@APP.route("/campaign/get_campaign", methods=["GET"])
# @jwt_required(fresh=False)
def get_campaign():
    # verify_jwt_in_request()

    name = request.json.get("name", None)
    id = request.json.get("id", None)

    return db_campaigns.get_campaign(name=name, id=id)


@APP.route("/campaign/get_campaigns", methods=["GET"])
# @jwt_required(fresh=False)
def get_all_campaigns():
    # verify_jwt_in_request()

    return db_campaigns.get_all_campaigns()


@APP.route("/campaign/register_collectible", methods=["POST"])
# @jwt_required(fresh=False)
def register_collectible():
    # verify_jwt_in_request()

    campaign_id = request.json.get("campaign_id", None)
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    image = request.json.get("image", None)
    collectible_fields = request.json.get("collectible_fields", None)

    return db_collectibles.register_collectible(
        campaign_id, name, description, image, collectible_fields
    )


@APP.route("/campaign/get_collectibles", methods=["GET"])
# @jwt_required(fresh=False)
def get_campaign_collectibles():
    # verify_jwt_in_request()

    campaign_id = request.json.get("campaign_id", None)

    return db_campaigns.get_campaign_collectibles(campaign_id)


@APP.route("/campaign/collectible_opt_fields", methods=["GET"])
# @jwt_required(fresh=False)
def get_campaign_opt_col_names():
    """Returns the optional columns for campain collectibles"""
    # verify_jwt_in_request()

    campaign_id = request.json.get("campaign_id", None)

    return db_campaigns.get_campaign_collectible_fields(campaign_id)


""" |------------------------------------|
    |         Collection Routes         |
    |------------------------------------| """


@APP.route("/collection", methods=["POST"])
@jwt_required(fresh=False)
def insert_collectible():
    user_id = get_jwt_identity()
    campaign_id = request.json.get("campaign_id", None)
    collectible_id = request.json.get("collectible_id", None)

    return db_collections.insert_collectible(user_id, campaign_id, collectible_id)


""" |------------------------------------|
    |           Wantlist Routes          |
    |------------------------------------| """


# TODO: Implement the wantlist function. Not sure how to select a users wantlist
#       Is the relational database set up so that each time a user is created, a wantlist
#       is instantiated. Or wantlist can be searched for and its contents retruned by
#       user id?
@APP.route("/wantlist", methods=["GET"])
@jwt_required(fresh=False)
def wantlist():
    user_id = get_jwt_identity()
    return jsonify(db_waintlist.get_wantlist(user_id)), OK


""" |------------------------------------|
    |           Dashboard Routes         |
    |------------------------------------| """

# Example stubs for /dashboard and /collection
# @APP.route('/dashboard', methods=['GET'])
# @jwt_required(fresh=False)
# def dashboard():
#     user_id = get_jwt_identity()
#     return jsonify(dbm.get_dashboard(user_id)), OK


""" |------------------------------------|
    |         Example JWT Routes         |
    |------------------------------------| """
# @APP.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     '''
#     Example of protected route. Requires JWT to access.
#     Useful for when user has been logged in for a while and wants to edit profile.
#     '''

#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), OK

# @APP.route("/protected_fresh", methods=["GET"])
# @jwt_required(fresh=True)
# def protected_fresh():
#     '''
#     Example of protected route. Requires fresh JWT to be fresh to access.
#     Useful for when user has been logged in for a while and wants to edit profile.
#     '''

#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), OK


if __name__ == "__main__":
    APP.run(host=config.host, port=config.port)
