import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_campaigns
import db_helpers
import db_collectibles
from main.error import OK, InputError, AccessError


""" |------------------------------------|
    |      Functions for collections     |
    |------------------------------------| """


def insert_collectible(user_id, collectible_id):
    """insert_collectible.

    Inserts a collectible to users collection

    Args:
        user_id: collectors id
        campaign_id: id of campaign which collectible belongs to
        collectible_id: id of collectible in campaign
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
    """remove_collectible.

    Removes a collection row from users collection

    Args:
        user_id: collectors id
        collection_id: id of collection entry corresponding to collectible to be removed.
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


# TODO: Error checking for invalid user id
def get_collection(collector_id):
    """get_collection.

    Return list conataining all collectibles and their details in users collection.

    Args:
        user_id: collectors user id

    get_collection() = {
        "collection": [
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
    # campains = db.Table("campaigns", metadata, autoload_with=engine)

    join = db.join(
        collections,
        collectibles,
        (collections.c.collectible_id == collectibles.c.id)
        & (collections.c.collector_id == collector_id),
    )

    select_stmt = db.select(
        collections.c.id.label("id"),
        collections.c.collectible_id.label("collectible_id"),
        collectibles.c.campaign_id.label("campaign_id"),
        collectibles.c.name.label("name"),
        collectibles.c.description.label("description"),
        collectibles.c.image.label("image"),
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


""" |------------------------------------|
    |  Helper Functions for collections  |
    |------------------------------------| """


def user_owns_collection(user_id, collection_id):
    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    select_stmt = db.select(collections).where(collections.c.id == collection_id)
    result = conn.execute(select_stmt)
    conn.close()

    return result.fetchone()._asdict().get("collector_id") == user_id


def get_last_collection(user_id):
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
