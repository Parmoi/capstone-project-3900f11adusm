import os

from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
)

from main import auth
from main.database import (
    db_campaigns,
    db_campaign_analytics,
    db_collectibles,
    db_collections,
    db_collectors,
    db_exchangehistory,
    db_manager as dbm,
    db_tradeoffers,
    db_tradeposts,
    db_wantlist,
)
from main.error import InputError, AccessError, OK
from main.privelage import ADMIN, MANAGER
from mock_data import mock_data_init
import helpers.config as config
import helpers.exceptions as exceptions

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


# @APP.route("/")
# def entry():
#     return "<h1>Hello, Collector<h1\>"

with APP.app_context():
    dbm.database_setup()

""" |------------------------------------|
    |          Database Routes           |
    |------------------------------------| """


@APP.route("/initdb")
def init_db():
    dbm.database_setup()
    return jsonify(msg="Database has been setup successfully!"), OK


# @APP.route("/init_mock_data", methods=["GET"])
# def init_mock_data():
#     return jsonify(msg="Mock data initialised!"), OK


@APP.route("/init_mock_data/demo", methods=["GET"])
def init_mock_data_demo():
    mock_data_init.generate_demo()

    return jsonify(msg="Mock data initialised!"), OK


""" |------------------------------------|
    |       Authentication Routes        |
    |------------------------------------| """


@APP.route("/login", methods=["POST"])
def login():
    """Logs the user into the system.

    Example Success Output:
        {"userId": 1, "privelage": 2}, 200
    
    Example Error Output:
        {"msg": "Invalid password!"}, 400
    """
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    return auth.login(email=email, password=password)


@APP.route("/logout", methods=["POST"])
def logout():
    """Logs the user out of the system.

    Example Success Output:
        {"msg": "Logout successful!"}, 200
    """
    return auth.logout()


@APP.route("/register", methods=["POST"])
def register():
    """Register a new user to the system.

    Example Success Output:
        {"msg": "Account successfully registered!", "user_id": 1}, 200

    Example Error Output:
        {"msg": "Email or username already registered!"}, 400
    """
    email = request.json.get("email", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    return auth.register_collector(
        email=email,
        username=username,
        password=password,
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


""" |------------------------------------|
    |          Collector Routes          |
    |------------------------------------| """


@APP.route("/profile", methods=["GET"])
@jwt_required(fresh=False)
def profile():
    """Fetch the profile of the desired user.

    Example Success Output:
        {
            "id": 1,
            "email": "bob@gmail.com",
            "username": "bobby",
            "first_name": "bob",
            "last_name": "junior",
            "phone": "0444444444",
            "address": "NSW",
            "profile_picture": "www.some_image.com/rnanranrrqn",
            "twitter_handle": "monkey",
            "facebook_handle": "monkey",
            "instagram_handle": "monkey"
        }, 200

    Example Error Output:
        {"msg": "Invalid collector id"}, 400
    """
    user_id = request.args.get("id")
    return db_collectors.get_collector(user_id=user_id)


@APP.route("/profile/update", methods=["POST"])
@jwt_required(fresh=False)
def profile_update():
    """Updates the profile details of the user.

    Example Success Output:
        {
            "msg": "Collector successfully updated!", 
            "collector": 
                {
                    "id": 1,
                    "email": "bob@gmail.com",
                    "username": "bobby",
                    "first_name": "bob",
                    "last_name": "junior",
                    "phone": "0444444444",
                    "address": "NSW",
                    "profile_picture": "www.some_image.com/rnanranrrqn",
                    "twitter_handle": "monkey",
                    "facebook_handle": "monkey",
                    "instagram_handle": "monkey"
                }
        }
    """

    user_id = get_jwt_identity()

    email = request.json.get("email", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    phone = request.json.get("phone", None)
    address = request.json.get("address", None)
    profile_picture = request.json.get("profile_picture", None)

    return db_collectors.update_collector(
        id=user_id,
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        password=password,
        address=address,
        profile_picture=profile_picture,
    )

@APP.route("/profile/update_socials", methods=["POST"])
@jwt_required(fresh=False)
def profile_socials_update():
    """Route specifically to update the socials of the user

    Example Success Output:
        {"msg": "User 1's socials have been updated}, 200
    """
    user_id = get_jwt_identity()
    twitter_handle = request.json.get("twitter_handle")
    facebook_handle = request.json.get("facebook_handle")
    instagram_handle = request.json.get("instagram_handle")

    return db_collectors.update_socials(
        user_id, twitter_handle, facebook_handle, instagram_handle)


@APP.route("/get_collectors", methods=["GET"])
def get_collectors():
    """Returns all the collectors within our database."""
    return db_collectors.get_all_collectors()


@APP.route("/search", methods=["GET"])
def first_search():
    """Returns all the collectibles within our database."""
    return db_collectibles.get_all_collectibles()


""" |------------------------------------|
    |           Campaign Routes          |
    |------------------------------------| """


@APP.route("/campaign/register", methods=["POST"])
@jwt_required(fresh=False)
def register_campaign():
    """Registers a campaign to our database."""
    verify_jwt_in_request()

    user_id = get_jwt_identity()
    name = request.json.get("name", None)
    description = request.json.get("desc", None)
    image = request.json.get("image", None)
    start_date = request.json.get("start", None)
    end_date = request.json.get("end", None)
    collectibles = request.json.get("collectibles_list", None)

    return db_campaigns.register_campaign(
        user_id, name, description, image, start_date, end_date
    )


@APP.route("/campaign/get_campaigns", methods=["GET"])
def get_all_campaigns():
    """Returns all campaigns stored in the database."""
    return db_campaigns.get_all_campaigns()


@APP.route("/campaign/register_collectible", methods=["POST"])
def register_collectible():
    """Register a collectible under the specified campaign."""
    campaign_id = request.json.get("campaign_id", None)
    collectible_name = request.json.get("name", None)
    description = request.json.get("description", None)
    image = request.json.get("image", None)

    return db_collectibles.register_collectible(
        campaign_id, collectible_name, description, image
    )


@APP.route("/campaign/get_collectibles", methods=["GET"])
@jwt_required(fresh=False)
def get_campaign_collectibles():
    """Return the collectibles associated with the passed in campaign_id."""
    campaign_id = request.args.get("campaign_id")

    return db_campaigns.get_campaign_collectibles(campaign_id)


@APP.route("/campaign/feedback", methods=["POST"])
@jwt_required(fresh=False)
def give_campaign_feedback():
    """Registers a user's feedback on a campaign."""
    verify_jwt_in_request()

    user_id = get_jwt_identity()
    campaign_id = request.json.get("campaign_id", None)
    feedback = request.json.get("feedback", None)

    return db_campaigns.add_campaign_feedback(user_id, campaign_id, feedback)


""" |------------------------------------|
    |         Collection Routes          |
    |------------------------------------| """


@APP.route("/collection/add", methods=["POST"])
@jwt_required(fresh=False)
def insert_collectible():
    """Inserts a collectible into the user's collection
    
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
    """Gets the collectibles that are in the user's collection."""
    user_id = get_jwt_identity()

    return db_collections.get_collection(user_id)


@APP.route("/collection/delete", methods=["DELETE"])
@jwt_required(fresh=False)
def remove_collectible():
    """Deletes a collectible from the user's collection.

    Args:
        user_id: int (collector's id)
        collection_id: int (id of entry to be deleted)

    Returns:
        {collection_id: int}
    """
    user_id = get_jwt_identity()
    collection_id = request.json.get("id", None)

    return db_collections.remove_collectible(user_id, collection_id)


# @APP.route("/collection/check", methods=["GET"])
# @jwt_required(fresh=False)
# def user_has_collectible():
#     """Checks if the user has a certain"""
#     user_id = get_jwt_identity()
#     collectible_id = request.json.get("collectible_id", None)

#     return db_collections.user_has_collectible(user_id, collectible_id)


""" |------------------------------------|
    |           Wantlist Routes          |
    |------------------------------------| """


@APP.route("/wantlist/get", methods=["GET"])
@jwt_required(fresh=False)
def wantlist():
    """
    Returns the list of collectibles inside the user's wantlist.

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
    Inserts a collectible into the user's wantlist
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
    Deletes a collectible from the user's wantlist

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
    Moves collectible from user's wantlist to their collection

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
        user_id, collection_id, post_title, post_desc, post_imgs
    )


@APP.route("/trade/view", methods=["GET"])
@jwt_required(fresh=False)
def get_tradepost():
    """
    Returns trade post information for a specific post
    Takes trade post id as param
    Used when we click on a trade post
    """
    trade_post_id = request.args.get("trade_post_id")

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


@APP.route("/exchange/makeoffer", methods=["POST"])
@jwt_required(fresh=False)
def make_offer():
    """
    Accepts parameters for an offer to a collectible setup for trade.
    """
    user_id = get_jwt_identity()
    trade_id = request.json.get("trade_id", None)
    offer_collection_id = request.json.get("collection_id", None)
    offer_msg = request.json.get("offer_message", None)
    offer_img = request.json.get("offer_img", None)

    return db_tradeoffers.register_trade_offer(
        trade_id, user_id, offer_collection_id, offer_msg, offer_img
    )


@APP.route("/exchange/decline", methods=["POST"])
@jwt_required(fresh=False)
def exchange_decline():
    """Declines the exchange offer for the trade item."""
    offer_id = request.json.get("offer_id", None)

    return db_tradeoffers.decline_trade_offer(offer_id)


@APP.route("/exchange/accept", methods=["POST"])
@jwt_required(fresh=False)
def exchange_accept():
    """Accepts the exchange offer for the trade item."""
    offer_id = request.json.get("offer_id", None)

    return db_tradeoffers.accept_trade_offer(offer_id)


""" |------------------------------------|
    |          Collectible Routes        |
    |------------------------------------| """


@APP.route("/collectible/get", methods=["GET"])
@jwt_required(fresh=False)
def get_collectible_info():
    """Find the information of a certain collectible.
    Takes in collectible_id as request argument

    stub_return = {
        "collectible_name": "Homer",
        "campaign_id": 1,
        "campaign_name": "Simpsons",
        "collectible_image": image_url
        "collectible_description": "Description",
        "collectible_added_date": "08/04/2003",
    }
    """
    user_id = get_jwt_identity()
    collectible_id = request.args.get("collectible_id", None)

    return db_collectibles.get_collectible_info(user_id, collectible_id)


@APP.route("/collectible/buy", methods=["GET"])
@jwt_required(fresh=False)
def get_trade_posts():
    """Finds the trade postings of a certain collectible."""
    collectible_id = request.args.get("collectible_id")

    return db_tradeposts.get_trade_posts(collectible_id)


""" |------------------------------------|
    |            Manager Routes          |
    |------------------------------------| """


@APP.route("/manager/invite", methods=["POST"])
@jwt_required(fresh=False)
def invite_manager():
    admin_id = get_jwt_identity()
    email = request.json.get("email", None)
    return auth.send_manager_email(admin_id, email)


@APP.route("/manager/analytics", methods=["GET"])
@jwt_required(fresh=False)
def get_manager_analytics():
    """
    Returns analytics of a campaigns posted by the given manager.

    If no campaigns are posted, or if no analytics are available, return an empty list.
    """
    manager_id = get_jwt_identity()

    return db_campaign_analytics.return_analytics(manager_id)


@APP.route("/manager/feedback", methods=["GET"])
@jwt_required(fresh=False)
def get_feedback():
    """Returns the feedback to the campaign manager for a campaign.

    Example Success Output:
        {
            "feedback": [
                {
                    "collector_id": 21,
                    "collector_username": "Barry",
                    "collector_profile_img": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                    "feedback": "I would have prefered if you didn't do another Simpsons campaign. Maybe try something with trees, trees are nice.",
                    "feedback_date": "2023/11/01",
                    "campaign_id": 2
                },
                {
                    "collector_id": 11,
                    "collector_username": "Bart",
                    "collector_profile_img": "https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api",
                    "feedback": "This is a good campaign, keep up the good work.",
                    "feedback_date": "2023/10/31",
                    "campaign_id": 5
                },
            ]
        }, 200
    """
    user_id = get_jwt_identity()

    return db_campaigns.get_campaign_feedback(user_id)


@APP.route("/manager/getlist", methods=["GET"])
@jwt_required(fresh=False)
def get_manager_list():
    """Returns a list of managers in the system.

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
                "canPublish": 3,  # The managers posting privilege
            },
            {
                "user_id": "2",
                "username": "szhang",
                "profile_img": "",
                "first_name": "Stella",
                "last_name": "Zhang",
                "email": "dz@gmail.com",
                "phone": "9999 4444",
                "privelage": 2,  # The managers posting privilege
            },
        ]
    }
    """
    return db_collectors.get_managers()


@APP.route("/manager/publish", methods=["POST"])
@jwt_required(fresh=False)
def manager_privilege():
    """
    Arguments:
        - manager_id

    Changes the campaign publishing privilege of a Manager.
    """

    stub_return = {"msg": "Manage privilege changed"}

    return jsonify(stub_return), OK


""" |------------------------------------|
    |      Admin Collector Routes        |
    |------------------------------------| """


@APP.route("/collector/getlist", methods=["GET"])
@jwt_required(fresh=False)
def get_collector_list():
    """
    Returns a list of collectors for the Admin to see

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
    """

    return db_collectors.get_all_collectors()


@APP.route("/collector/ban", methods=["POST"])
@jwt_required(fresh=False)
def ban_collector():
    """Bans a collector account, actionable only by an Admin

    Argument:
        - collector_id
    """

    admin_id = get_jwt_identity()
    collector_id = request.json.get("collector_id", None)

    db_collectors.ban_collector(admin_id, collector_id)

    stub_return = {"msg": "Collector banned."}

    return jsonify(stub_return), OK


@APP.route("/admin/get_campaigns", methods=["GET"])
@jwt_required(fresh=False)
def get_campaigns_for_review():
    """Provides a list of campaigns, either reviewed or not for the Admin to view and review.

    stub_return = {
        "campaigns": [
            {
                "campaign_id": "1",
                "campaign_name": "The Cats",
                "campaign_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw4xHiYs4vnhBs9jqjYk0_JY3-SiSavqovXA&usqp=CAU",
                "campaign_description": "The cats are new series of really cool collectibles that you can collect from us.",
                "campaign_start_date": "29/11/2023",
                "campaign_end_date": "12/12/2023",
                "collection_list": [
                    {
                        "collectible_id": "1",
                        "name": "Cat Cat",
                        "image": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                        "caption": "A super Cat",
                    },
                    {
                        "collectible_id": "2",
                        "name": "Doomed Dog",
                        "image": "https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api",
                        "caption": "A cat that is afraid",
                    },
                    {
                        "collectible_id": "3",
                        "name": "Lion Cat",
                        "image": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                        "caption": "Lioness Cat",
                    },
                    {
                        "collectible_id": "4",
                        "name": "Cat the Dog",
                        "image": "'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw4xHiYs4vnhBs9jqjYk0_JY3-SiSavqovXA&usqp=CAU'",
                        "caption": "A super duper cat and dog",
                    },
                ],
                "approved": False,
            },
            {
                "campaign_id": "2",
                "campaign_name": "The Dogs",
                "campaign_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw4xHiYs4vnhBs9jqjYk0_JY3-SiSavqovXA&usqp=CAU",
                "campaign_description": "The dogs are new series of really cool collectibles that you can collect from us.",
                "campaign_start_date": "29/11/2023",
                "campaign_end_date": "12/12/2023",
                "collection_list": [
                    {
                        "collectible_id": "1",
                        "name": "Dog Cat",
                        "image": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                        "caption": "A super Dog",
                    },
                    {
                        "collectible_id": "2",
                        "name": "Doomed Lion",
                        "image": "https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api",
                        "caption": "A Dog that is afraid",
                    },
                    {
                        "collectible_id": "3",
                        "name": "Lion Dog",
                        "image": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                        "caption": "Lion Dog",
                    },
                    {
                        "collectible_id": "4",
                        "name": "Dog the Cat",
                        "image": "'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw4xHiYs4vnhBs9jqjYk0_JY3-SiSavqovXA&usqp=CAU'",
                        "caption": "A super duper dog and cat",
                    },
                ],
                "approved": True,
            },
        ]
    }
    """
    return db_campaigns.get_campaigns_and_collectibles()


@APP.route("/admin/campaign/approve", methods=["POST"])
@jwt_required(fresh=False)
def admin_campaign_approve():
    """An Admin Approves the campaign.

    stub_return = {
        "msg" : "Campaign Approved"
    }
    """
    admin_id = get_jwt_identity()
    campaign_id = request.json.get("campaign_id", None)

    return db_campaigns.approve_campaign(admin_id, campaign_id)


@APP.route("/admin/campaign/decline", methods=["POST"])
@jwt_required(fresh=False)
def admin_campaign_decline():
    """An Admin Declines the campaign.

    stub_return = {
        "msg" : "Campaign declined!"
    }
    """
    admin_id = get_jwt_identity()
    campaign_id = request.json.get("campaign_id", None)

    return db_campaigns.decline_campaign(admin_id, campaign_id)


if __name__ == "__main__":
    APP.run(host=config.host, port=config.port)
