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


# TODO: Error checking for invalid user id
def get_collection(user_id):
    """get_collection.

    Return list conataining all collectibles in users collection.

    Args:
        user_id: collectors user id

    get_collection() = {
        "collection": [
            {
                "id": collection_id,
                "name": collectible_name,
                "description": collectible_description,
                "image": collectible_image,
                "campaign_id": campaign_id,
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
    for collection in collection_list:
        collectible = db_collectibles.get_collectible(
            collection.get("campaign_id"), collection.get("collectible_id")
        )
        # collectible.update("")
        collection.append(collec)

    return jsonify({"collection": collection_list}), OK


""" |------------------------------------|
    |  Helper Functions for collections  |
    |------------------------------------| """
