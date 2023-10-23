import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
from main.error import OK, InputError, AccessError


""" |------------------------------------|
    |      Functions for collections     |
    |------------------------------------| """


# TODO: Error checks for validity of all arguments
# TODO: Retrun name of collectible and campaign to return string
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

    if db_collectibles.find_collectible_id(campaign_id, collectible_id) is None:
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


# TODO: Error checking for invalid user id
def get_collection(user_id):
    """get_collection.

    Return list conataining all collectibles in users collection.

    Args:
        user_id: collectors user id
    """
    engine, conn, metadata = dbm.db_connect()
    collections = db.Table("collections", metadata, autoload_with=engine)
    select_stmt = db.select(collections).where(collections.c.collector_id == user_id)
    results = conn.execute(select_stmt).fetchall()
    conn.close()

    collection_list = [row._asdict() for row in results]

    return jsonify({"collection": collection_list}), OK


""" |------------------------------------|
    |  Helper Functions for collections  |
    |------------------------------------| """

