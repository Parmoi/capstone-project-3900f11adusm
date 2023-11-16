from main.privelage import ADMIN, MANAGER
from main.database import db_collectibles
import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
from main import auth
import db_helpers
from datetime import date, datetime
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |       Functions for campaigns      |
    |------------------------------------| """


def register_campaign(
    user_id,
    name,
    description,
    image,
    start_date,
    end_date,
    collectibles,
    approved=False,
):
    """insert_campaign.

    Function to insert new campaign.
    Dynamically creates campaign collectible table with optional fields.

    Args:
        name: name of collectible campaign
        description: description of collectible campaign
        start_date: start_date of campaign ("DD/MM/YYYY")
        end_date: end date of campaign ("DD/MM/YYYY")
        collectible_fields: list of fields/columns for collectibles in this campaign
    """
    if not auth.check_user_privelage(user_id, MANAGER):
        return (
            jsonify({"msg": "User does not have privelage level required!"}),
            AccessError,
        )

    start_date_obj = datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date_obj = datetime.strptime(end_date, "%d/%m/%Y").date()

    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    insert_stmt = db.insert(campaigns).values(
        {
            "name": name,
            "description": description,
            "image": image,
            "manager_id": user_id,
            "start_date": start_date_obj,
            "end_date": end_date_obj,
            "approved": approved,
        }
    )
    conn.execute(insert_stmt)
    conn.close()

    for collectible in collectibles:
        db_collectibles.register_collectible()

    return (
        jsonify(
            {
                "msg": "Campaign successfully registered!",
                "campaign_id": get_campaign_id(name),
            }
        ),
        OK,
    )


def approve_campaign(admin_id, campaign_id):
    if not auth.check_user_privelage(admin_id, ADMIN):
        return (
            jsonify({"msg": "User does not have privelage level required!"}),
            AccessError,
        )

    engine, conn, metadata = dbm.db_connect()
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)
    update_stmt = (
        db.update(campaigns)
        .where(campaigns.c.id == campaign_id)
        .values({"approved": True})
    )
    conn.execute(update_stmt)
    conn.close()
    return jsonify({"msg": "Campaign apporoved!"}), OK


def decline_campaign(admin_id, campaign_id):
    if not auth.check_user_privelage(admin_id, ADMIN):
        return (
            jsonify({"msg": "User does not have privelage level required!"}),
            AccessError,
        )

    engine, conn, metadata = dbm.db_connect()
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)
    update_stmt = (
        db.update(campaigns)
        .where(campaigns.c.id == campaign_id)
        .values({"approved": False})
    )
    conn.execute(update_stmt)
    conn.close()
    return jsonify({"msg": "Campaign declined!"}), OK


def get_campaign(name=None, id=None):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = None
    if name:
        select_stmt = db.select(campaigns).where(campaigns.c.name == name)
    elif id:
        select_stmt = db.select(campaigns).where(campaigns.c.id == id)
    else:
        return None

    execute = conn.execute(select_stmt)
    campaign = execute.fetchone()._asdict()
    conn.close()

    return jsonify(campaign), 200


# TODO: Error checking, Docstring
def get_all_campaigns():
    engine, conn, metadata = dbm.db_connect()

    campaigns = db.Table("campaigns", metadata, autoload_with=engine)
    select_stmt = db.select(campaigns).where(campaigns.c.approved == True)
    results = conn.execute(select_stmt)
    conn.close()

    all_campaign_rows = results.all()
    campaigns = [row._asdict() for row in all_campaign_rows]

    return jsonify({"campaigns": campaigns}), 200


# TODO: Error checking, Docstring
def get_campaign_collectibles(campaign_id):
    """get_campaign_collectibles.

    Args:
        campaign_id:

    Returns:
    collectibles = {
        "collectibles": [
            {
                "id": 1,
            },
        ]
    }
    """

    engine, conn, metadata = dbm.db_connect()

    collectibles = db.Table("collectibles", metadata, autoload_with=engine)

    select_stmt = db.select(collectibles).where(
        collectibles.c.campaign_id == campaign_id
    )
    results = conn.execute(select_stmt)
    conn.close()

    all_collectible_rows = results.all()
    collectibles = [row._asdict() for row in all_collectible_rows]

    return (
        jsonify(
            {
                "collectibles": collectibles,
            }
        ),
        OK,
    )


def get_campaigns_and_collectibles():
    """
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
    """

    engine, conn, metadata = dbm.db_connect()

    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(
        campaigns.c.id.label("campaign_id"),
        campaigns.c.name.label("campaign_name"),
        campaigns.c.image.label("campaign_image"),
        campaigns.c.description.label("campaign_description"),
        campaigns.c.start_date.label("campaign_start_date"),
        campaigns.c.end_date.label("campaign_end_date"),
        campaigns.c.approved.label("approved"),
    ).select_from(campaigns)

    campaigns = conn.execute(select_stmt)
    campaigns = db_helpers.rows_to_list(campaigns.fetchall())

    campaign_list = []
    for campaign in campaigns:
        campaign_id = campaign.get("campaign_id")
        select_stmt = (
            db.select(
                collectibles.c.id.label("collectible_id"),
                collectibles.c.name.label("name"),
                collectibles.c.image.label("image"),
                collectibles.c.description.label("caption"),
            )
            .where(collectibles.c.campaign_id == campaign_id)
            .select_from(collectibles)
        )
        campaign_collectibles = conn.execute(select_stmt)
        campaign["collection_list"] = db_helpers.rows_to_list(campaign_collectibles)
        campaign_list.append(campaign)

    conn.close()

    return (
        jsonify(
            {
                "campaigns": campaign_list,
            }
        ),
        OK,
    )

    all_collectible_rows = results.all()
    collectibles = [row._asdict() for row in all_collectible_rows]


def get_campaigns_in_period(time_period):
    """Function to return campaigns depending on the time_period entered.

    Args:
        time_period (string): ("past", "current", "future") specifies what time
                              period we want the campaigns from

    Return:
        JSON, int: JSON that holds a list of campaigns (or our error message),
                   int is the error code

    Expected Output:
        {"campaigns":
            [
                {
                    "id": 1,
                    "name": "random",
                    "image": null,
                    "description": "potato",
                    "start_date": "30/12/2020"
                    "end_date": "30/12/2025",
                },
                {
                    "id": 4,
                    "name": "campaign 3",
                    "image": null,
                    "description": "random desc",
                    "start_date": "01/01/1999"
                    "end_date": "01/01/2025",
                },
            ]
        }, OK
    """

    # Error checking for valid time_period input
    valid_periods = ["past", "current", "future"]

    if time_period not in valid_periods:
        return jsonify({"msg": "Invalid time_period entered."}), InputError

    engine, conn, metadata = dbm.db_connect()

    camp = db.Table("campaigns", metadata, autoload_with=engine)

    cur_date = date.today()
    search_stmt = db.select(camp)

    # Generate a search statement depending on the period we want
    if time_period == "past":
        search_stmt = db.select(camp).where(camp.c.end_date <= cur_date)
    elif time_period == "current":
        search_stmt = db.select(camp).where(
            (camp.c.start_date <= cur_date) & (camp.c.end_date > cur_date)
        )
    else:
        search_stmt = db.select(camp).where(camp.c.start_date > cur_date)

    # Finds the list of campaigns
    campaign_list = db_helpers.rows_to_list(conn.execute(search_stmt).fetchall())
    conn.close()

    return jsonify({"campaigns": campaign_list}), OK


def add_campaign_feedback(user_id, campaign_id, feedback):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    feedback_table = db.Table("campaign_feedback", metadata, autoload_with=engine)

    cur_date = date.today()

    insert_stmt = db.insert(feedback_table).values(
        {
            "campaign_id": campaign_id,
            "collector_id": user_id,
            "feedback": feedback,
            "feedback_date": cur_date,
        }
    )
    conn.execute(insert_stmt)
    conn.close()

    return (
        jsonify(
            {
                "msg": "Campaign feedback successfully added!",
            }
        ),
        OK,
    )


def get_campaign_feedback(user_id):
    """
    Returns the feedback to the campaign manager for a campaign.

    stub_return = {
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
    }
    """
    engine, conn, metadata = dbm.db_connect()

    feedback = db.Table("campaign_feedback", metadata, autoload_with=engine)
    collectors = db.Table("collectors", metadata, autoload_with=engine)
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    join = db.join(
        collectors, feedback, (collectors.c.id == feedback.c.collector_id)
    ).join(campaigns, (feedback.c.campaign_id == campaigns.c.id))

    select_stmt = (
        db.select(
            collectors.c.id.label("collector_id"),
            collectors.c.username.label("collector_username"),
            collectors.c.profile_picture.label("collector_profile_img"),
            feedback.c.campaign_id,
            feedback.c.feedback,
            feedback.c.feedback_date
            # campaigns.c.id.label("campaign_id")
        )
        .select_from(join)
    )

    res = conn.execute(select_stmt)
    if res is None:
        return jsonify({"msg": "Campaign id does not exist!"}), InputError
    else:
        feedback_list = db_helpers.rows_to_list(res.fetchall())
        return jsonify({"feedback": feedback_list}), OK


""" |------------------------------------|
    |   Helper functions for campaigns   |
    |------------------------------------| """


# Function to convert campaign name to campaign id
# Returns campaign id as int
def get_campaign_id(campaign_name):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.id).where(campaigns.c.name == campaign_name)

    execute = conn.execute(select_stmt)
    campaign_id = execute.fetchone()._asdict().get("id")
    conn.close()

    return campaign_id


def get_campaign_name(campaign_id):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.name).where(campaigns.c.id == campaign_id)

    execute = conn.execute(select_stmt)
    campaign_id = execute.fetchone()._asdict().get("name", None)
    conn.close()

    return campaign_id
