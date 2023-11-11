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
    db_tradeposts,
    db_tradeoffers
)
from main import auth
from main.error import InputError, AccessError, OK
from main.privelage import ADMIN, MANAGER
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
    return jsonify(msg="Mock data initialised!"), OK


@APP.route("/init_mock_data/demo", methods=["GET"])
def init_mock_data_demo():
    mock_data_init.generate_demo()

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


@APP.route("/privelage/get", methods=["GET"])
@jwt_required(fresh=True)
def get_privelage():
    user_id = get_jwt_identity()
    return auth.get_privelage(user_id)


@APP.route("/privelage/update", methods=["POST"])
@jwt_required(fresh=True)
def update_privelage():
    user_id = get_jwt_identity()
    privelage = request.json.get("privelage", None)
    return auth.update_privelage(user_id, privelage)


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
    # search_query = request.json.get("query", None)
    # return db_collectibles.search_collectibles(search_query)
    # return db_campaigns.get_campaign_collectibles(1)
    return db_collectibles.get_all_collectibles()


""" |------------------------------------|
    |           Campaign Routes          |
    |------------------------------------| """


@APP.route("/campaign/register", methods=["POST"])
# @jwt_required(fresh=False)
def register_campaign():
    # verify_jwt_in_request()

    name = request.json.get("name", None)
    description = request.json.get("desc", None)
    image = request.json.get("image", None)
    start_date = request.json.get("start", None)
    end_date = request.json.get("end", None)

    return db_campaigns.register_campaign(
        name, description, image, start_date, end_date
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
    """
    Inserts collectible into collection list
    Returns collection id created

    Args:
        user_id: UUID
        collectible_id: int
    """
    user_id = get_jwt_identity()
    collectible_id = request.json.get("collectible_id", None)

    return db_collections.insert_collectible(user_id, collectible_id)


@APP.route("/collection/get", methods=["GET"])
@jwt_required(fresh=False)
def get_collection():
    user_id = get_jwt_identity()
    return db_collections.get_collection(user_id)
    # return jsonify([
    #     {
    #         'id': 1,
    #         'name': 'Homer',
    #         'campaign_name': 'Simpsons',
    #         'campaign_id': 1,
    #         'collectible_id': 1,
    #         'image': 'https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg',
    #         'date_added': '23/05/2014',
    #         'date_released': '03/03/2014',
    #     },
    #     {
    #         "id": 2,
    #         "image": 'https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api',
    #         "name": 'Marge',
    #         'campaign_id': 12,
    #         'collectible_id': 12,
    #         "campaign_name": 'Winter 2022',
    #         'date_added': '03/02/2014',
    #         'date_released': '03/01/2014',
    #     },
    #     {
    #         "id": 3,
    #         "image": 'https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api',
    #         "name": 'Bart',
    #         'campaign_id': 1,
    #         'collectible_id': 2,
    #         "campaign_name": 'Simpsons',
    #         'date_added': '03/08/2014',
    #         'date_released': '03/01/2014',
    #     },
    # ]), 200


@APP.route("/collection/delete", methods=["DELETE"])
@jwt_required(fresh=False)
def remove_collectible():
    """
    Deletes collectible from user's collection

    Args:
        user_id: int (collector's id)
        collection_id: int (id of entry to be deleted)

    Returns {
        collection_id: int
    }
    """

    # return jsonify({'collection_id': 1}), 200
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


@APP.route("/wantlist/get", methods=["GET"])
@jwt_required(fresh=False)
def wantlist():
    """
    Returns list of collectibles in user's want list along with details about collectible to be displayed

    Args:
        user_id: collectors user id

    Returns:
    [
        {
            id: int, (wantlist_id)
            campaign_id: int,
            collectible_id: int,
            name: str, (name of collectible)
            image: str, (collectible image url)
            campaign_name: str,
            date_released: "DD/MM/YYYY", (date collection/campaign was released)
            date_added: "DD/MM/YYYY", (date collectible was added to wantlist)
        },
        ...
    ]
    """
    user_id = get_jwt_identity()

    return db_wantlist.get_wantlist(user_id)


@APP.route("/wantlist/add", methods=["POST"])
@jwt_required(fresh=False)
def insert_wantlist():
    """
    Inserts collectible into wantlist
    Returns wantlist id created

    Args:
        user_id: UUID
        collectible_id: int

    Returns:
    {
        'wantlist_id': int
    }
    """
    user_id = get_jwt_identity()
    collectible_id = request.json.get("collectible_id", None)

    return db_wantlist.insert_wantlist(user_id, collectible_id)


@APP.route("/wantlist/delete", methods=["DELETE"])
@jwt_required(fresh=False)
def remove_wantlist():
    """
    Deletes collectible from user's wantlist

    Args:
        user_id: int (collector's id)
        wantlist: int (id of entry to be deleted)

    Returns {
        wantlist_id: int
    }
    """
    user_id = get_jwt_identity()
    wantlist_id = request.json.get("wantlist_id", None)

    return db_wantlist.remove_from_wantlist(user_id, wantlist_id)


@APP.route("/wantlist/move", methods=["POST"])
@jwt_required(fresh=False)
def move_collectible():
    """
    Moves collectible from user's wantlist to collection

    Args:
        user_id: int (collector's id)
        wantlist_id: int (id of entry to be moved)

    Returns {
        collection_id: int (id of new entry created in collection)
    }
    """

    user_id = get_jwt_identity()
    wantlist_id = request.json.get("wantlist_id", None)

    return db_wantlist.move_to_collection(user_id, wantlist_id)


""" |------------------------------------|
    |           Trade Routes             |
    |------------------------------------| """


@APP.route("/trade/post", methods=["POST"])
@jwt_required(fresh=False)
def post_trade():
    """
    Creates trade post, returns post_id

    Args:
        collection_id
        post_title
        post_description
        post_images: [] (list of post image urls dictionaries: {name, caption, image})

    """

    user_id = get_jwt_identity()
    collection_id = request.json.get("collection_id")
    post_title = request.json.get("post_title")
    post_desc = request.json.get("post_description")
    post_imgs = request.json.get("post_images")

    return db_tradeposts.insert_trade_post(
        user_id, collection_id, post_title, post_desc, post_imgs)


@APP.route("/trade/view", methods=["GET"])
@jwt_required(fresh=False)
def get_tradepost():
    """
    Returns trade post information
    Takes trade post id as param

    """
    trade_post_id = request.args.get('trade_post_id')

    return db_tradeposts.get_trade_post_info(trade_post_id)

@APP.route("/tester")
def tester():
    db_collections.insert_collectible(1, 2)
    db_collections.insert_collectible(2, 3)
    db_collections.insert_collectible(3, 5)
    db_tradeposts.insert_trade_post(1, 501, "random post!", "random desc!", [{
                "name": "1",
                "caption": "Bart with skateboard.",
                "image": "https://tse1.mm.bing.net/th?id=OIP.S9zFPgPbF0zJ4OXQkU675AHaHC&pid=Api",
            },
            {
                "name": "2",
                "caption": "Stuffed bart.",
                "image": "https://tse1.mm.bing.net/th?id=OIP.AIizpaWw4l8TtY5fWj66RgHaGr&pid=Api",
            }])
    db_tradeoffers.register_trade_offer(1, 2, 502, 1, 501)
    db_tradeoffers.register_trade_offer(1, 3, 503, 1, 501)
    # return db_tradeposts.get_current_trade_posts(1)
    # return db_tradeoffers.find_tradelist_offers(1) # find trade going to id 1
    return db_tradeoffers.find_outgoing_offers(2)

@APP.route("/trade/list", methods=["GET"])
@jwt_required(fresh=False)
def tradelist():
    """
    Displays all the trades listed from the collector
    that have received an offer of exchange from another collector.

    """

    stub_data = {
        "trades_list": [
            {
                "trader_collectible_id": 1,
                "trader_collectible_name": "Bart with skateboard",  # collectible you're givin away
                "trader_collectible_img": "https://tse1.mm.bing.net/th?id=OIP.S9zFPgPbF0zJ4OXQkU675AHaHC&pid=Api",  # image of the collectible you're giving away.
                "offer_id": 1,
                "offer_collectible_id": 2,
                "offer_collectible_name": "Stuffed bart",
                "offer_collectible_img": "https://tse1.mm.bing.net/th?id=OIP.AIizpaWw4l8TtY5fWj66RgHaGr&pid=Api",
                "offer_collector_id": 3,  # id of the collector sending the offer
                "offer_profile_img": "https://tse1.mm.bing.net/th?id=OIP.ho7hCKNowRHh7u5wu1aMWQHaF9&pid=Api",  # The profile image of the collector sending the offer
                "offer_name": "person2",
                "offer_made_date": "02/06/2003",
            }
        ]
    }

    return jsonify(stub_data), OK


""" |------------------------------------|
    |           Offers Routes            |
    |------------------------------------| """


@APP.route("/offers/get", methods=["GET"])
@jwt_required(fresh=False)
def offers_get():
    stub_data = {
        "offers_list": [
            {
                "offer_id": "",
                "collectible_id": "",
                "collectible_name": "Homer",
                "offer_status": "SENT",  # status can be SENT, ACCEPTED or DECLINED
                "collectible_img": "",
                "trader_collector_id": "",  # id of the collector offer was sent to
                "trader_profile_img": "",  # The profile image of the other collector that offer was sent to
                "trader_name": "person2",
                "date_offer": "02/06/2003",
                "date_updated": "02/06/2004",
            }
        ]
    }

    return jsonify(stub_data), OK


""" |------------------------------------|
    |           Exchange Routes          |
    |------------------------------------| """


@APP.route("/exchange/history", methods=["GET"])
@jwt_required(fresh=False)
def exchange_history():
    user_id = get_jwt_identity()

    stub_return = {  # return a json list
        "exchange_history": [
            {
                "exchange_id": "2",
                "traded_collectible_id": "1",
                "traded_collectible_name": "Homer",
                "traded_collectible_img": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                "traded_campaign_id": "1",
                "traded_campaign_name": "Simpsons",
                "traded_campaign_img": "",
                "accepted_collectible_id": "2",
                "accepted_collectible_name": "Marge",
                "accepted_collectible_img": "https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api",
                "accepted_campaign_id": 1,
                "accepted_campaign_name": "Simpsons",
                "accepted_campaign_img": "",
                "trader_collector_id": "2",
                "trader_profile_img": "default",
                "trader_username": "person2",
                "offer_made_date": "2023/10/25",
                "accepted_date": "2023/10/29",
            },
            {
                "exchange_id": "3",
                "traded_collectible_id": "1",
                "traded_collectible_name": "Bart",
                "traded_collectible_img": "https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api",
                "traded_campaign_id": "1",
                "traded_campaign_name": "Simpsons",
                "traded_campaign_img": "",
                "accepted_collectible_id": "2",
                "accepted_collectible_name": "Dog",
                "accepted_collectible_img": "https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api",
                "accepted_campaign_id": 1,
                "accepted_campaign_name": "Simpsons",
                "accepted_campaign_img": "",
                "trader_collector_id": "2",
                "trader_profile_img": "default",
                "trader_username": "person2",
                "offer_made_date": "2023/10/25",
                "accepted_date": "2023/10/29",
            },
        ]
    }

    return jsonify(stub_return), OK


@APP.route("/exchange/available", methods=["GET"])
@jwt_required(fresh=False)
def available_exchanges():
    user_id = get_jwt_identity()

    collectible_id = request.json.get("collectible_id", None)

    stub_return = {  # return a json list
        "trade_posts": [
            {
                "trade_id": "",  # ID of the posted trade, will be used for making offers to the trade.
                "collector_id": "",  # The collector who posted the trade
                "collector_username": "",
                "collectible_id": collectible_id,
                "collectible_name": "",
                "item_img": "",  # collector uploaded image. irl image
                "creation_date": "",
                "post_title": "",
                "suggested_worth": "",
                "description": "",  # collector uploaded description
            }
        ]
    }

    return jsonify(stub_return), OK


@APP.route("/exchange/makeoffer", methods=["POST"])
@jwt_required(fresh=False)
def make_offer():
    """
    Accepts parameters for an offer to a collectible setup for trade.
    Should store the information as a
    """
    user_id = get_jwt_identity()  # collector making the offer for trade

    trade_id = request.json.get(
        "trade_id", None
    )  # ID of the trade the collector is making an offer to.
    offer_collectible_id = request.json.get("collectible_id", None)
    description = request.json.get("description", None)  # description of offer.
    offer_img = request.json.get(
        "offer_img", None
    )  # offer maker uploaded image of collectible they're offering for the trade.
    offer_title = request.json.get(
        "offer_title", None
    )  # title of the offer being made for the trade item.

    stub_return = {"msg": "Offer has been successfully sent."}

    return jsonify(stub_return), OK


@APP.route("/exchange/decline", methods=["POST"])
@jwt_required(fresh=False)
def exchange_decline():
    """
    Declines the exchange offer for the trade item.
    """

    user_id = get_jwt_identity()
    offer_id = request.json.get("offer_id", None)

    stub_data = {"msg": "offer successfully declined"}

    return jsonify(stub_data), OK


@APP.route("/exchange/accept", methods=["POST"])
@jwt_required(fresh=False)
def exchange_accept():
    """
    Accepts the exchange offer for the trade item.
    """

    user_id = get_jwt_identity()
    offer_id = request.json.get("offer_id", None)

    stub_data = {"msg": "offer successfully accepted"}

    return jsonify(stub_data), OK


""" |------------------------------------|
    |          Collectible Routes        |
    |------------------------------------| """


@APP.route("/collectible/get", methods=["GET"])
@jwt_required(fresh=False)
def get_collectible_info():
    """
    Takes in collectible_id as request argument
    """
    # user_id = get_jwt_identity()

    stub_return = {
        "collectible_name": "Homer",
        "campaign_id": 1,
        "campaign_name": "Simpsons",
        "collectible_image": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
        "collectible_description": "Description",
        "collectible_added_date": "08/04/2003",
    }

    return jsonify(stub_return), OK


@APP.route("/collectible/buy", methods=["GET"])
@jwt_required(fresh=False)
def get_buylist():
    """
    Takes in collectible_id as request argument
    """

    # I'm not too sure how to get the collectible_id from frontend, but if you 
    # call get_trade_posts with collectible_id it should work properly - Dyllan
    collectible_id = request.args.get('collectible_id')
    
    return db_tradeposts.get_trade_posts(collectible_id)


""" |------------------------------------|
    |            Manager Routes          |
    |------------------------------------| """


@APP.route("/manager/feedback", methods=["GET"])
@jwt_required(fresh=False)
def get_feedback():
    """
    Returns the feedback to the campaign manager for a campaign.
    """

    stub_return = {
        "feedback": [
            {
                "collector_id": 21,
                "collector_username": "Barry",
                "collector_profile_img": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                "feedback": "I would have prefered if you didn't do another Simpsons campaign. Maybe try something with trees, trees are nice.",
                "feedback_date": "2023/11/01",
            },
            {
                "collector_id": 11,
                "collector_username": "Bart",
                "collector_profile_img": "https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api",
                "feedback": "This is a good campaign, keep up the good work.",
                "feedback_date": "2023/10/31",
            },
        ]
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
