import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
from datetime import date
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |       Functions for campaigns      |
    |------------------------------------| """


def register_campaign(name, description, start_date, end_date):
    """insert_campaign.

    Function to insert new campaign.
    Dynamically creates campaign collectible table with optional fields.

    Args:
        name: name of collectible campaign
        description: description of collectible campaign
        start_date: start_date of campaign ("YYYY-MM-DD")
        end_date: end date of campaign ("YYYY-MM-DD")
        collectible_fields: list of fields/columns for collectibles in this campaign
    """

    start_date_obj = date.fromisoformat(start_date)
    end_date_obj = date.fromisoformat(end_date)

    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    insert_stmt = db.insert(campaigns).values(
        {
            "name": name,
            "description": description,
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
    """
    Function to return campaigns depending on the time_period entered.

    Args:
    - time_period: specify what time period we want the campaigns from (past/current/future)

    Expected Output:
    {"campaigns":
    [
        {
            "collectibles_table":"mock collectibles",
            "description":"random desc",
            "end_date":"Wed, 01 Jan 2025 00:00:00 GMT",
            "id":3,
            "image":"https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
            "name":"mock",
            "start_date":"Fri, 01 Jan 1999 00:00:00 GMT"
        },
        {
            "collectibles_table":"campaign 4_collectibles",
            "description":"random desc",
            "end_date":"Tue, 01 Jan 2030 00:00:00 GMT",
            "id":4,
            "image":"https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
            "name":"campaign 4",
            "start_date":"Fri, 01 Jan 1999 00:00:00 GMT"
        }
    ]}
    """

    # Error checking for valid time_period input
    valid_periods = ["past", "current", "future"]

    if time_period not in valid_periods:
        return jsonify({"msg": "Invalid time_period entered."}), InputError

    engine, conn, metadata = dbm.db_connect()

    camp = db.Table("campaigns", metadata, autoload_with=engine)

    cur_date = date.today()
    search_stmt = db.select(camp)

    if time_period == "past":
        search_stmt = db.select(camp).where(camp.c.end_date <= cur_date)
    elif time_period == "current":
        search_stmt = db.select(camp).where(
            (camp.c.start_date <= cur_date) & (camp.c.end_date > cur_date)
        )
    else:
        search_stmt = db.select(camp).where(camp.c.start_date > cur_date)

    execute = conn.execute(search_stmt)
    conn.close()

    result_list = []
    results = execute.fetchall()

    for row in results:
        result_list.append(row._asdict())

    return jsonify({"campaigns": result_list}), OK


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
