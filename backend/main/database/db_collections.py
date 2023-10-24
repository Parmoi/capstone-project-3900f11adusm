import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_campaigns
import db_collectibles
from main.error import OK, InputError, AccessError


""" |------------------------------------|
    |      Functions for collections     |
    |------------------------------------| """


def insert_collectible(user_id, campaign_id, collectible_id):
    """insert_collectible.

    Inserts a collectible to users collection

    Args:
        user_id: collectors id
        campaign_id: id of campaign which collectible belongs to
        collectible_id: id of collectible in campaign
    """

    campaign_coll_table = db_campaigns.get_campaign_coll_table(campaign_id)
    if campaign_coll_table is None:
        return (
            jsonify(
                {
                    "msg": "Collectible campaign {} not valid id!".format(campaign_id),
                }
            ),
            InputError,
        )

    if db_collectibles.get_collectible(campaign_id, collectible_id) is None:
        return (
            jsonify(
                {
                    "msg": "Colletible {} in campain {} does not exist!".format(
                        collectible_id, campaign_id
                    ),
                }
            ),
            InputError,
        )

    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    insert_stmt = db.insert(collections).values(
        {
            "collector_id": user_id,
            "campaign_id": campaign_id,
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
def get_collection(user_id):
    """get_collection.

    Return list conataining all collectibles and their details in users collection.

    Args:
        user_id: collectors user id

    get_collection() = {
        "collection": [
            {
                "id": collection_id,
                "campaign_id": campaign_id,
                "collectible_id": collectible_id,
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
    select_stmt = db.select(collections).where(collections.c.collector_id == user_id)
    results = conn.execute(select_stmt)
    conn.close()

    if results is None:
        return (
            jsonify(
                {
                    "msg": "User {}'s collection is empty!".format(user_id),
                }
            ),
            InputError,
        )

    rows = results.fetchall()
    collection_rows = [row._asdict() for row in rows]

    # for collection in collection_list:
    # [db_collectibles.get_collectible(collection.get("campaign_id"), collection.get("collectible_id"))).update("collection_id"=collection.get("id")} for collection in collection_list]
    collection = []
    for collection_row in collection_rows:
        collectible = db_collectibles.get_collectible(
            collection_row.get("campaign_id"), collection_row.get("collectible_id")
        )
        collectible["collectible_id"] = collectible.pop("id")
        collectible.update(id=collection_row.get("id"))
        collection.append(collectible)

    return jsonify({"collection": collection}), OK


def user_has_collectible(user_id, campaign_id, collectible_id):
    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    exists_criteria = (
        db.select(collections)
        .where(
            (collections.c.collector_id == user_id)
            & (collections.c.campaign_id == campaign_id)
            & (collections.c.collectible_id == collectible_id)
        )
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
    select_stmt = db.select(collections).where(collections.c.id == user_id)
    result = conn.execute(select_stmt)
    conn.close()

    return result.fetchone()._asdict().get("collector_id") == user_id
