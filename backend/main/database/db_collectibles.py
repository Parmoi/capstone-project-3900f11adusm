import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_campaigns
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |     Functions for collectibles     |
    |------------------------------------| """


# TODO: Error checking
def register_collectible(campaign_id, name, description, image, collectible_fields):
    """register_collectible.

    Register a collectible in a campaign.

    Args:
        campaign_id: id of campaign collectible belongs to
        name: name of collectible
        description: description of collectible
        image: Image URL of collectible
        collectible_fields: dictionary of optional fields
    """

    collectible_dict = {
        "name": name,
        "description": description,
        "image": image,
        "campaign_id": campaign_id,
    } | collectible_fields

    coll_table_name = db_campaigns.get_campaign_coll_table(campaign_id)

    engine, conn, metadata = dbm.db_connect()
    collectibles = db.Table(coll_table_name, metadata, autoload_with=engine)
    insert_stmt = db.insert(collectibles).values(collectible_dict)

    conn.execute(insert_stmt)
    conn.close()

    return (
        jsonify(
            {
                "msg": "Collectible succesfully registered!",
                "campaign_id": campaign_id,
                "collectible_id": find_collectible_id(campaign_id, name),
            }
        ),
        OK,
    )


""" |------------------------------------|
    |  Helper functions for collectibles |
    |------------------------------------| """


def get_collectible(campaign_id, collectible_id):
    """get_collectible.

    Args:
        campaign_id:
        collectible_id:
    """

    collectible_table_name = db_campaigns.get_campaign_coll_table(campaign_id)

    engine, conn, metadata = dbm.db_connect()
    collectibles = db.Table(collectible_table_name, metadata, autoload_with=engine)
    select_stmt = db.select(collectibles).where(collectibles.c.id == collectible_id)
    result = conn.execute(select_stmt)
    conn.close()

    if result is None:
        return None

    return result.fetchone()._asdict()


# Function to convert collectible name to collectible id
# Returns collection id as int
def find_collectible_id(campaign_id, collectible_name):
    engine, conn, metadata = dbm.db_connect()

    collectible_table_name = db_campaigns.get_campaign_coll_table(campaign_id)
    # Loads in the campaign table into our metadata
    collectibles = db.Table(collectible_table_name, metadata, autoload_with=engine)

    select_stmt = db.select(collectibles.c.id).where(
        collectibles.c.name == collectible_name
    )

    execute = conn.execute(select_stmt)
    collectible_id = execute.fetchone()._asdict().get("id")
    conn.close()

    # TODO: Value error if doesn't exist or return error code or something?

    return collectible_id


def search_collectibles(collectible_name):
    """
    Function to return collectibles whose name matches the collectible_name

    Example Output:
    [
        {
            "campaign_name": "random campaign",
            "collectible_name": "collectible 1",
            "collectible_image": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
            "date_released": "Fri, 01 Jan 2021 00:00:00 GMT"
        },
        {
            "campaign_name": "random campaign",
            "collectible_name": "collectible 2",
            "collectible_image": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
            "date_released": "Fri, 01 Jan 2021 00:00:00 GMT"
        }
    ]

    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectible and campaign tables into our metadata
    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)
    coll = collectibles.alias("coll")
    camp = campaigns.alias("camp")

    joined_tbl = db.join(coll, camp, coll.c.campaign_id == camp.c.id)

    search_stmt = (
        db.select(
            camp.c.name.label("campaign_name"),
            coll.c.name.label("collectible_name"),
            camp.c.start_date.label("date_released"),
            coll.c.image.label("collectible_image")
        )
        .select_from(joined_tbl)
        .where(coll.c.name == collectible_name)
    )

    execute = conn.execute(search_stmt)
    conn.close()

    result_list = []
    results = execute.fetchall()

    for row in results:
        result_list.append(row._asdict())

    return result_list
