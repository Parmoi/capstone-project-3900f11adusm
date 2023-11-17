from flask import jsonify
import sqlalchemy as db

from main.error import OK, InputError
import db_helpers, db_manager as dbm

""" |------------------------------------|
    |     Functions for collectibles     |
    |------------------------------------| """


def register_collectible(campaign_id, collectible_name, description, image):
    """Register a collectible to a campaign.

    Args:
        campaign_id (int): id of campaign collectible belongs to
        name (string): name of collectible
        description (string): description of collectible
        image (string): Image URL of collectible
    
    Returns:
        JSON: contains operation message, campaign_id and collectible_id
    """
    collectible_dict = {
        "name": collectible_name,
        "description": description,
        "image": image,
        "campaign_id": campaign_id,
    }

    engine, conn, metadata = dbm.db_connect()
    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    insert_stmt = db.insert(collectibles).values(collectible_dict)
    conn.execute(insert_stmt)
    conn.close()

    return (
        jsonify(
            {
                "msg": "Collectible {} succesfully registered!".format(
                    collectible_name
                ),
                "campaign_id": campaign_id,
                "collectible_id": find_collectible_id(collectible_name),
            }
        ),
        OK,
    )


def get_collectible_info(user_id, collectible_id):
    """Finds the collectible information for a collectible.

    Args:
        user_id (int): id of the user
        collectible_id (int): id of collectible we want to get info for

    Returns:
        JSON:
            - on success: dictionary of our collectible information
            - on error: error message
    """
    engine, conn, metadata = dbm.db_connect()
    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    join = db.join(
        collectibles, campaigns, 
        (collectibles.c.campaign_id == campaigns.c.id) &
        (collectibles.c.id == collectible_id)
    )

    select_stmt = db.select(
        collectibles.c.name.label("collectible_name"),
        campaigns.c.id.label("campaign_id"),
        campaigns.c.name.label("campaign_name"),
        collectibles.c.image.label("collectible_image"),
        collectibles.c.description.label("collectible_description"),
        campaigns.c.start_date.label("date_added"),
    ).select_from(join)

    res = conn.execute(select_stmt)

    if res is None:
        return jsonify({"msg": "Invalid collectible id"}), InputError
    else:
        return jsonify(res.fetchone()._asdict()), OK    


def get_all_collectibles():
    """Returns all collectibles that are in our database.

    Returns:
        JSON: list of collectibles and their information
    """
    engine, conn, metadata = dbm.db_connect()
    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    join = db.join(
        collectibles, campaigns, (collectibles.c.campaign_id == campaigns.c.id)
    )

    select_stmt = db.select(
        collectibles.c.id.label("id"),
        collectibles.c.name.label("collectible_name"),
        collectibles.c.image.label("collectible_image"),
        collectibles.c.description.label("collectible_description"),
        campaigns.c.name.label("campaign_name"),
        campaigns.c.start_date.label("date_released"),
    ).select_from(join)

    coll_list = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())

    return jsonify({"collectibles": coll_list}), OK


""" |------------------------------------|
    |  Helper functions for collectibles |
    |------------------------------------| """


def get_collectible(collectible_id):
    """Returns a collectible's information.

    Args:
        collectible_id (int): id of the collectible we want id for
    
    Returns:
        dictionary: dictionary containing the collectible's information
    """
    engine, conn, metadata = dbm.db_connect()

    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    select_stmt = db.select(collectibles).where(collectibles.c.id == collectible_id)
    result = conn.execute(select_stmt)
    conn.close()

    if result is None:
        return {}

    return result.fetchone()._asdict()


def find_collectible_id(collectible_name):
    """Finds the id of the collectible with name collectible_name

    Args:
        collectible_name (string): name of collectible

    Returns:
        int: the id of the collectible
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectibles table
    coll = db.Table("collectibles", metadata, autoload_with=engine)

    # Finds and returns the id associated with the collectible_name
    select_stmt = db.select(coll).where(coll.c.name == collectible_name)
    execute = conn.execute(select_stmt)

    return execute.fetchone()._asdict().get("id")

