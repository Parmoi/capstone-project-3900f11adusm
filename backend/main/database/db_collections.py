import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_campaigns
import db_helpers
import db_collectibles
from main.error import OK, InputError, AccessError
from datetime import date, datetime


""" |------------------------------------|
    |      Functions for collections     |
    |------------------------------------| """


def insert_collectible(user_id, collectible_id):
    """Inserts a collectible to a user's collection.

    Args:
        user_id (int): id of collector whose collection we want to add to
        collectible_id (int): id of collectible we want to add to the collection
    
    Returns:
        JSON: Either the success/error message
        int: success/error code
    """
    collectible = db_collectibles.get_collectible(collectible_id)

    if collectible is None:
        return (
            jsonify(
                {
                    "msg": "Colletible {} does not exist!".format(collectible_id),
                }
            ),
            InputError,
        )

    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    insert_stmt = db.insert(collections).values(
        {
            "collector_id": user_id,
            "collectible_id": collectible_id,
            "date_added": date.today(),
        }
    )
    result = conn.execute(insert_stmt)
    conn.close()

    if result is None:
        return (
            jsonify(
                {
                    "msg": "Collectible {} unable to be added to collection!".format(
                        collectible_id
                    ),
                }
            ),
            InputError,
        )
    else:
        return (
            jsonify(
                {
                    "msg": "Collectible {} successfully added to collection!".format(
                        collectible_id
                    ),
                }
            ),
            OK,
        )


def remove_collectible(user_id, collection_id):
    """Removes a collectible from the user's collection

    Args:
        user_id (int): id of collector that we want to remove collectible from collection from
        collection_id (int): id of collection that we want to remove
    
    Returns:
        JSON: success/error message
        int: success/error code
    """

    if not user_owns_collection(user_id, collection_id):
        return (
            jsonify(
                {
                    "msg": "User {} does not own collection {}".format(
                        user_id, collection_id
                    ),
                }
            ),
            InputError,
        )

    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)

    dlt_stmt = db.delete(collections).where(collections.c.id == collection_id)
    result = conn.execute(dlt_stmt)
    conn.close()

    return (
        jsonify(
            {
                "msg": "Collection row {} successfully removed to collection!".format(
                    collection_id
                ),
            }
        ),
        OK,
    )


def get_collection(collector_id):
    """Returns a list of collectibles and their details in the user's collection

    Args:
        user_id (int): id of collector we want to find the collection for

    Returns:
        JSON:
            - on success: list of colllectibles in collection
            - on error: error message
        int: success/error code
        
    Example Output:
        {"collection": [
            {
                "id": collection_id,
                "collectible_id": collectible_id,
                "campaign_id": campaign_id,
                "name": collectible_name,
                "description": collectible_description,
                "image": collectible_image,
                ... ()
            },
        ],
    }
    """

    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    campaigns = db.Table("campaigns", metadata, autoload_with=engine)

    join = db.join(
        collections,
        collectibles,
        (collections.c.collectible_id == collectibles.c.id)
        & (collections.c.collector_id == collector_id),
    ).join(campaigns, collectibles.c.campaign_id == campaigns.c.id)

    select_stmt = db.select(
        collections.c.id.label("id"),
        collections.c.collectible_id.label("collectible_id"),
        collections.c.date_added.label("date_added"),
        collectibles.c.campaign_id.label("campaign_id"),
        collectibles.c.name.label("name"),
        collectibles.c.description.label("description"),
        collectibles.c.image.label("image"),
        campaigns.c.name.label("campaign_name"),
        campaigns.c.start_date.label("date_released")
    ).select_from(join)

    results = conn.execute(select_stmt)
    conn.close()

    if results is None:
        return (
            jsonify(
                {
                    "msg": "User {}'s collection is empty!".format(collector_id),
                }
            ),
            InputError,
        )

    rows = results.fetchall()

    collection = db_helpers.rows_to_list(rows)

    return jsonify({"collection": collection}), OK


def user_has_collectible(user_id, collectible_id):
    """Checks if a user has a certain collectible in their collection.

    Args:
        user_id (int): id of collector whose collection we want to check
        collectible_id (int): id of collectible we want to check its existence

    Returns:
        JSON: success/error message
    """
    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    exists_criteria = db.select(collections).where(
        (collections.c.collector_id == user_id)
        & (collections.c.collectible_id == collectible_id)
    )
    stmt = db.exists(exists_criteria).select()
    result = conn.execute(stmt)
    conn.close()
    return (
        jsonify(
            {
                "msg": result.fetchone()._asdict().get("anon_1"),
            }
        ),
        OK,
    )


def move_collectible(sender_id, receiver_id, collection_id):
    """Moves a collectible from the sender's collection to the receiver's collection
    
    Args:
        sender_id (int): id of collector that owns the collectible
        receiver_id (int): id of collector that will receive the collectible
        collection_id (int): id of collection that will be moved
    
    Returns:
        JSON, int: JSON of success/error message, int of success/error code

    Example Output:
        {"msg": "Collectible has successfully been moved!}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collections and collectibles table
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)

    # Find id of collectible associated with the collection
    join = db.join(ctn, cbl,
        (ctn.c.collectible_id == cbl.c.id) & (ctn.c.id == collection_id))
    
    select_stmt = (db.select(
        cbl.c.id.label("collectible_id")
    )).select_from(join)

    # Find the collectible id, remove the collection from sender, and add to collection of receiver
    collectible_id = conn.execute(select_stmt).fetchone()._asdict().get("collectible_id")
    remove_collectible(sender_id, collection_id)
    insert_collectible(receiver_id, collectible_id)
    conn.close()

    return jsonify({"msg": "Collectible has successfully been moved!"}), OK

""" |------------------------------------|
    |  Helper Functions for collections  |
    |------------------------------------| """


def user_owns_collection(user_id, collection_id):
    """Returns whether collection belongs to the user

    Args:
        user_id (int): id of collector we want to check
        collection_id (int): id of collection we want to check if it is owned by the collector

    Returns:
        boolean: whether or not the collection_id is linked to that user
    """
    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    select_stmt = db.select(collections).where(collections.c.id == collection_id)
    result = conn.execute(select_stmt)
    conn.close()

    return result.fetchone()._asdict().get("collector_id") == user_id


def get_last_collection(user_id):
    """Get the last collection entry for a certain user.

    Args:
        user_id (int): id of user that we want to get the last collection entry for

    Returns:
        dictionary: dictionary of the details of the last collection entry
    """
    engine, conn, metadata = dbm.db_connect()

    collections = db.Table("collections", metadata, autoload_with=engine)
    select_stmt = (
        db.select(collections)
        .where(collections.c.collector_id == user_id)
        .order_by(collections.c.id.desc())
    )
    results = conn.execute(select_stmt)
    conn.close()

    collection_dict = results.fetchone()._asdict()
    return collection_dict

def get_collectible_id(collection_id):
    """Find the collectible_id from the collection_id

    Args:
        collection_id (int): id of the collection we want to find a collectible_id for
    
    Returns:
        int: int of the collectible_id from the collection_id

    Example Output:
        2
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collection and collectible tables
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)

    join = db.join(ctn, cbl,
        (ctn.c.collectible_id == cbl.c.id) & (ctn.c.id == collection_id))
    
    select_stmt = (db.select(
        cbl.c.id.label("collectible_id")
    )).select_from(join)

    # Find the collectible id
    collectible_id = conn.execute(select_stmt).fetchone()._asdict().get("collectible_id")
    conn.close()

    return collectible_id
