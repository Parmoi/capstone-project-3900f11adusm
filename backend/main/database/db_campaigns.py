import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
from datetime import date
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |       Functions for campaigns      |
    |------------------------------------| """


def register_campaign(name, description, start_date, end_date, collectible_fields):
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

    collectibles_table_name = name + "_collectibles"
    # Adds campaign to campaigns table
    insert_stmt = db.insert(campaigns).values(
        {
            "name": name,
            "collectibles_table": collectibles_table_name,
            "description": description,
            "start_date": start_date_obj,
            "end_date": end_date_obj,
        }
    )
    conn.execute(insert_stmt)

    collectible_table = db.Table(
        collectibles_table_name,
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("name", db.String, unique=True),
        db.Column("description", db.String),
        db.Column("image", db.String),
        db.Column("campaign_id", db.Integer, db.ForeignKey("campaigns.id")),
        * (db.Column(collectible_col) for collectible_col in collectible_fields),
    )

    metadata.create_all(engine)
    conn.close()

    # Create collectible table for this campaign.

    return (
        jsonify(
            {
                "msg": "Campaign successfully registered!",
                "campaign_id": find_campaign_id(name),
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


""" |------------------------------------|
    |   Helper functions for campaigns   |
    |------------------------------------| """


def get_campaign_coll_table(campaign_id):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectible and belongs_to table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.collectible_table).where(
        campaigns.c.id == campaign_id
    )

    execute = conn.execute(select_stmt)
    collectible_table = execute.fetchone()._asdict().get("collectible_table")


# Function to convert campaign name to campaign id
# Returns campaign id as int
def find_campaign_id(campaign_name):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.id).where(campaigns.c.name == campaign_name)

    execute = conn.execute(select_stmt)
    campaign_id = execute.fetchone()._asdict().get("id")
    conn.close()

    return campaign_id


def find_campaign_name(campaign_id):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.name).where(campaigns.c.id == campaign_id)

    execute = conn.execute(select_stmt)
    campaign_id = execute.fetchone()._asdict().get("name", None)
    conn.close()

    return campaign_id
