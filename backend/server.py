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
    db_wantlist,
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
    """
    returns:
        {
        profile_picture: "string",
        Username: "string",
        first_name: "string",
        last_name: "string",
        email: "email_string",
        phone: "string" (numbers),
        address: "string"
        }
    """
    user_id = get_jwt_identity()
    return db_collectors.get_collector(user_id=user_id)


@APP.route("/profile/update", methods=["POST"])
@jwt_required(fresh=False)
def profile_update():
    """
    Updates the profile details of the user. Returns detailed
    error messages if the user provides invalid data.
    
    Example: "username already taken"

    Args:
        profile_picture: string
        username: string
        email: valid email format.
        first_name: string
        last_name: string
        phone: string (numbers) 
        address: string
    """

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


@APP.route("/search", methods=["GET"])
def first_search():
    search_query = request.json.get("query", None)
    # return db_collectibles.search_collectibles(search_query)
    return db_campaigns.get_campaign_collectibles(1)


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
    collectible_name = request.json.get("name", None)
    description = request.json.get("description", None)
    image = request.json.get("image", None)

    return db_collectibles.register_collectible(
        campaign_id, collectible_name, description, image
    )


@APP.route("/campaign/get_collectibles", methods=["GET"])
# @jwt_required(fresh=False)
def get_campaign_collectibles():
    # verify_jwt_in_request()

    campaign_id = request.json.get("campaign_id", None)

    return db_campaigns.get_campaign_collectibles(campaign_id)


""" |------------------------------------|
    |         Collection Routes          |
    |------------------------------------| """


@APP.route("/collection/add", methods=["POST"])
@jwt_required(fresh=False)
def insert_collectible():
    user_id = get_jwt_identity()
    collectible_id = request.json.get("collectible_id", None)

    return db_collections.insert_collectible(user_id, collectible_id)


@APP.route("/collection/get", methods=["GET"])
@jwt_required(fresh=False)
def get_collection():
    user_id = get_jwt_identity()
    return db_collections.get_collection(user_id)


@APP.route("/collection/delete", methods=["DELETE"])
@jwt_required(fresh=False)
def remove_collectible():
    user_id = get_jwt_identity()
    collection_id = request.json.get("id", None)

    return db_collections.remove_collectible(user_id, collection_id)


@APP.route("/collection/check", methods=["GET"])
@jwt_required(fresh=False)
def user_has_collectible():
    user_id = get_jwt_identity()
    collectible_id = request.json.get("collectible_id", None)

    return db_collections.user_has_collectible(user_id, collectible_id)


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
    return jsonify(db_wantlist.get_wantlist(user_id)), OK

""" |------------------------------------|
    |           Exchange Routes          |
    |------------------------------------| """

@APP.route("/exchange/history", methods=["GET"])
@jwt_required(fresh=False)
def exchange_history():
    user_id = get_jwt_identity()

    stub_return = {     # return a json list
        "exchange_history" : [{
            "exchange_id": "",
            "traded_collectible_id": "",
            "traded_collectible_name": "",
            "traded_collectible_img": "",
            "traded_campaign_id": "",
            "traded_campaign_name": "",
            "traded_campaign_img": "",
            "accepted_collectible_id": "",
            "accepted_collectible_name": "",
            "accepted_collectible_img": "",
            "accepted_campaign_id": "",
            "accepted_campaign_name": "",
            "accepted_campaign_img": "",
            "trader_collector_id": "",      # The id of the other collector, not the collector viewing
            "trader_profile_img": "",       # The profile image of the other collector
            "trader_username": "person2",
            "offer_made_date": "2023/10/25",
            "accepted_date": "2023/10/29",        
        }] 
    }

    return jsonify(stub_return), OK

@APP.route("/exchange/available", methods=["GET"])
@jwt_required(fresh=False)
def available_exchanges():
    user_id = get_jwt_identity()

    collectible_id = request.json.get("collectible_id", None)

    stub_return = {     # return a json list
        "trade_posts" : [{
            "trade_id": "",             # ID of the posted trade, will be used for making offers to the trade.
            "collector_id": "",         # The collector who posted the trade
            "collector_username": "",
            "collectible_id": collectible_id,
            "collectible_name": "",
            "item_img": "",             # collector uploaded image. irl image
            "creation_date": "",
            "post_title": "",
            "suggested_worth": "",
            "description": ""           # collector uploaded description
        }] 
    }

    return jsonify(stub_return), OK


@APP.route("/exchange/makeoffer", methods=["POST"])
@jwt_required(fresh=False)
def make_offer():
    """
    Accepts parameters for an offer to a collectible setup for trade.
    Should store the information as a 
    """
    user_id = get_jwt_identity()       # collector making the offer for trade


    trade_id = request.json.get("trade_id", None)               # ID of the trade the collector is making an offer to.
    offer_collectible_id = request.json.get("collectible_id", None)
    description = request.json.get("description", None)         # description of offer.
    offer_img = request.json.get("offer_img", None)             # offer maker uploaded image of collectible they're offering for the trade.
    offer_title = request.json.get("offer_title", None)         # title of the offer being made for the trade item.


    stub_return = {
        "msg": "Offer has been successfully sent."
    }

    return jsonify(stub_return), OK

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
