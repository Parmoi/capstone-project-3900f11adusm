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
    db_tradeoffers,
    db_exchangehistory
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
    user_id = request.args.get('id')

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
        post_images: [] (list of post image urls dictionaries: {caption, image})

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
    Used when we click on a trade post

    """
    trade_post_id = request.args.get('trade_post_id')

    return db_tradeposts.get_trade_post_info(trade_post_id)


@APP.route("/trade/list", methods=["GET"])
@jwt_required(fresh=False)
def tradelist():
    """
    Displays all the trades listed from the collector and number of offers made
    to each trade
    """
    user_id = get_jwt_identity()

    return db_tradeposts.get_current_trade_posts(user_id)

@APP.route("/trade/list/offers", methods=["GET"])
@jwt_required(fresh=False)
def trade_offers_list():
    """
    Displays all the trades listed from the collector and number of offers made
    Takes in trade post id

    """
    trade_post_id = request.args.get("trade_id")
    return db_tradeoffers.find_tradelist_offers(trade_post_id)


""" |------------------------------------|
    |           Offers Routes            |
    |------------------------------------| """


@APP.route("/offers/get", methods=["GET"])
@jwt_required(fresh=False)
def offers_get():
    user_id = get_jwt_identity()
    return db_tradeoffers.find_outgoing_offers(user_id)


""" |------------------------------------|
    |           Exchange Routes          |
    |------------------------------------| """


@APP.route("/exchange/history", methods=["GET"])
@jwt_required(fresh=False)
def exchange_history():
    """
    Find the user's exchange history
    """
    user_id = get_jwt_identity()
    return db_exchangehistory.find_exchange_history(user_id)


@APP.route("/exchange/available", methods=["GET"])
@jwt_required(fresh=False)
def available_exchanges():
    """
    I think this function might be unnecessary - Dyllan
    """
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

    trade_id = request.json.get("trade_id", None)
    offer_collection_id = request.json.get("collection_id", None)
    offer_msg = request.json.get("offer_message", None)
    offer_img = request.json.get("offer_img", None)
    # There's also description, but I don't need it

    return db_tradeoffers.register_trade_offer(
        trade_id, user_id, offer_collection_id, offer_msg, offer_img)


@APP.route("/exchange/decline", methods=["POST"])
@jwt_required(fresh=False)
def exchange_decline():
    """
    Declines the exchange offer for the trade item.
    """
    offer_id = request.json.get("offer_id", None)

    return db_tradeoffers.decline_trade_offer(offer_id)


@APP.route("/exchange/accept", methods=["POST"])
@jwt_required(fresh=False)
def exchange_accept():
    """
    Accepts the exchange offer for the trade item.
    """
    offer_id = request.json.get("offer_id", None)

    return db_tradeoffers.accept_trade_offer(offer_id)


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


@APP.route("/manager/analytics", methods=["GET"])
@jwt_required(fresh=False)
def get_manager_analytics():
    """
    Returns analytics of a campaigns posted by the
    given manager. 

    If no campaigns are posted, or if no analytics 
    are available, return an empty list.
    """

    manager_id = get_jwt_identity()

    stub_return = {
        "analytics": [
            {
                "campaign_id": 21,
                "campaign_name": "Simpsons",

                # Essentially the X-axes labels
                "exchange_dates": ['2023/10/20', '2023/10/21', '2023/10/22', '2023/10/23', '2023/10/24', '2023/10/25', '2023/10/26'],   
                # Essentially the y-axes data for the X-axes labels
                "exchanges_made": [24, 13, 98, 39, 48, 38, 43]  # These two lists need to be the same length
            },
            {
                "campaign_id": 22,
                "campaign_name": "Simpsons 2",
                "exchange_dates": ['2023/11/20', '2023/11/21', '2023/11/22', '2023/11/23', '2023/11/24', '2023/11/25', '2023/11/26'],
                "exchanges_made": [26, 23, 78, 19, 88, 76, 14]
            },
        ]
    }

    return jsonify(stub_return), OK

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


@APP.route("/manager/invite", methods=["POST"])
@jwt_required(fresh=False)
def invite_manager():
    """
    Arguments:
        - email

    Sends the given email account an email with a registration code and
    a link to http://localhost:3000/register/manager for registration.
    """

    stub_return = {
        "msg": "An invite has been sent."
    }

    return jsonify(stub_return), OK


@APP.route("/manager/register", methods=["POST"])
@jwt_required(fresh=False)
def register_manager():
    """
    Arguments:
        - username
        - first_name
        - last_name
        - email
        - phone
        - password
        - special_code

    A special registration that registers Manager accounts.
    Manager privilege should be that of not postable.
    """

    stub_return = {
        "msg": "Registration successful"
    }

    return jsonify(stub_return), OK

@APP.route("/manager/getlist", methods=["GET"])
@jwt_required(fresh=False)
def get_manager_list():
    """
    Returns a list of managers in the system.
    """

    stub_return = {
        "managers": [
            {
                "user_id": "3",
                "username": "dso",
                "profile_img": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                "first_name": "Dyllanson",
                "last_name": "So",
                "email": "ds@gmail.com",
                "phone": "4444 4444",
                "canPublish": True,  # The managers posting privilege
            },
            {
                "user_id": "2",
                "username": "szhang",
                "profile_img": "",
                "first_name": "Stella",
                "last_name": "Zhang",
                "email": "dz@gmail.com",
                "phone": "9999 4444",
                "canPublish": False,  # The managers posting privilege
            },
        ]
    }

    return jsonify(stub_return), OK

@APP.route("/manager/publish", methods=["POST"])
@jwt_required(fresh=False)
def manager_privilege():
    """
    Arguments:
        - manager_id
        - can_publish

    Changes the campaign publishing privilege of a Manager.
    """

    stub_return = {
        "msg": "Manage privilege changed"
    }

    return jsonify(stub_return), OK

""" |------------------------------------|
    |      Admin Collector Routes        |
    |------------------------------------| """


@APP.route("/collector/getlist", methods=["GET"])
@jwt_required(fresh=False)
def get_collector_list():
    """
    Returns a list of collectors for the Admin to see
    """

    stub_return = {
        "collectors": [
            {
                "user_id": "3",
                "username": "gwhite",
                "profile_img": "",
                "first_name": "Greg",
                "last_name": "Whitehead",
                "email": "gw@gmail.com",
                "phone": "4444 4444",
            },
            {
                "user_id": "2",
                "username": "meng",
                "profile_img": "",
                "first_name": "Meng",
                "last_name": "Xiao",
                "email": "mx@gmail.com",
                "phone": "7777 4444",
            },
        ]
    }

    return jsonify(stub_return), OK

@APP.route("/collector/ban", methods=["POST"])
@jwt_required(fresh=False)
def ban_collector():
    """
    Argument:
        - collector_id

    Bans a collector account, actionable only by an Admin
    """

    stub_return = {
        "msg": "Collector banned."
    }

    return jsonify(stub_return), OK

@APP.route("/admin/get_campaigns", methods=["GET"])
@jwt_required(fresh=False)
def get_campaigns_for_review():
    """
    

    Provides a list of campaigns, either reviewed or not
    for the Admin to view and review.
    """

    stub_return = {
        "campaigns": [
            {
                "campaign_id": '1',
                "campaign_name": 'The Cats',
                "campaign_image": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw4xHiYs4vnhBs9jqjYk0_JY3-SiSavqovXA&usqp=CAU',
                "campaign_description": 'The cats are new series of really cool collectibles that you can collect from us.',
                "campaign_start_date": '29/11/2023',
                "campaign_end_date": '12/12/2023',
                "collection_list": [
                    {
                        "collectible_id": "1",
                        "collectible_name": "Tiger Cat",
                        "collectible_image": "data:image/jpeg;base64,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"
                    },
                    {
                        "collectible_id": "2",
                        "collectible_name": "Scaredy Cat",
                        "collectible_image": "data:image/jpeg;base64,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"
                    },
                    {
                        "collectible_id": "3",
                        "collectible_name": "Lion Cat",
                        "collectible_image": "data:image/jpeg;base64,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"
                    },
                    {
                        "collectible_id": "4",
                        "collectible_name": "Cat the Cat",
                        "collectible_image": "data:image/jpeg;base64,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"
                    },
                ]

            },
        ]
    }

    return jsonify(stub_return), OK

@APP.route("/admin/campaign/approve", methods=["POST"])
@jwt_required(fresh=False)
def admin_campaign_approve():
    """
    An Admin Approves the campaign. 
    """

    campaign_id = request.json.get("campaign_id", None)

    stub_return = {
        "msg" : "Campaign Approved" 
    }

    return jsonify(stub_return), OK

@APP.route("/admin/campaign/decline", methods=["POST"])
@jwt_required(fresh=False)
def admin_campaign_decline():
    """
    An Admin Declines the campaing.
    """

    campaign_id = request.json.get("campaign_id", None)

    stub_return = {
        "msg" : "Campaign Declined" 
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
