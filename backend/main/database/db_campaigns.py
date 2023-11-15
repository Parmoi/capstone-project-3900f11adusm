import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_helpers
from datetime import date, datetime
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |       Functions for campaigns      |
    |------------------------------------| """


def register_campaign(user_id, name, description, image, start_date, end_date):
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
        }
    )
    conn.execute(insert_stmt)
    conn.close()

    return (
        jsonify(
            {
                "msg": "Campaign successfully registered!",
                "campaign_id": get_campaign_id(name),
            }
        ),
        OK,
    )


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
    select_stmt = db.select(campaigns)
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
    """
    collectibles = {
        "collectibles": [
            {
                "id": 1,
            },
        ]
    }
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
        200,
    )


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


def get_campaign_feedback(user_id, campaign_id):
    engine, conn, metadata = dbm.db_connect()

    feedback = db.Table("campaign_feedback", metadata, autoload_with=engine)
    collectors = db.Table("collectors", metadata, autoload_with=engine)

    join = db.join(collectors, feedback, (collectors.c.id == feedback.c.collector_id))

    select_stmt = (
        db.select(
            collectors.c.id.label("collector_id"),
            collectors.c.username.label("collector_username"),
            collectors.c.profile_picture.label("collector_profile_img"),
            feedback.c.feedback,
            feedback.c.feedback_date,
        )
        .select_from(join)
        .where(
            feedback.c.campaign_id == campaign_id,
        )
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
