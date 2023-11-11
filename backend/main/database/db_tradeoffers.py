import sqlalchemy as db
from flask import jsonify
import db_helpers
import db_manager as dbm
from error import OK, InputError, AccessError
from datetime import date

# TODO: Error checking
def register_trade_offer(trade_post_id, sender_id, ctn_s_id, receiver_id, ctn_r_id):
    """Generates a new trade offer for a certain trade_post

    Args:
        trade_post_id (int): id of the trade post that we making an offer for
        sender_id (int): id of collector that is sending the trade offer
        ctn_s_id (int): (collection_send_id) id of collectible in collection to send
        receiver_id (int): id of collector that is receiving the trade offer
        ctn_r_id (int): (collection_receive_id) id of collectible in collection trade for
    
    Returns:
        JSON, int: JSON of the trade offer's id, int of the error code
    
    Example Output:
        {"trade_offer_id": 1}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers table
    to = db.Table("trade_offers", metadata, autoload_with=engine)

    insert_stmt = db.insert(to).values(
        {
            "trade_post_id": trade_post_id,
            "trade_sender_id": sender_id,
            "collection_send_id": ctn_s_id,
            "trade_receiver_id": receiver_id,
            "collection_receive_id": ctn_r_id,
            "offer_status": "SENT",
            "date_offered": date.today()
        })
    conn.execute(insert_stmt)
    conn.close()

    # Find the id associated with the trade offer
    trade_offer_id = find_trade_offer_id(trade_post_id, sender_id, ctn_s_id, receiver_id, ctn_r_id)
    
    return jsonify({"trade_offer_id": trade_offer_id}), OK

# TODO: Error checking
def find_tradelist_offers(trade_post_id):
    """Finds all incoming offers for a certain trade post (when we click on it)

    Notes:
        - to be used by "trade_offers_list" API route

    Args:
        trade_post_id (int): id of trade post that we want to find offers for

    Returns:
        JSON, int: JSON of list of offers, int of error code
    
    Example Output:
       {
            [
                {
                    "offer_collectible_img": "https://robohash.org/voluptatemetipsum.png?size=50x50&set=set1",
                    "offer_collectible_name": "Phascogale calura",
                    "offer_id": 1,
                    "offer_made_date": "10/11/2023",
                    "trader_profile_img": "https://robohash.org/cumqueaccusamusvoluptas.png?size=50x50&set=set1",
                    "trader_username": "uamar"
                },
                {
                    "offer_collectible_img": "https://robohash.org/estcumquedebitis.png?size=50x50&set=set1",
                    "offer_collectible_name": "Ictonyx striatus"
                    "offer_id": 2,
                    "offer_made_date": "10/11/2023",
                    "trader_profile_img": "https://robohash.org/nesciuntculpaat.png?size=50x50&set=set1",
                    "trader_username": "szhang"
                }
            ]
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers, collections, collectibles, and collectors table
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    join = db.join(to, ctr, 
            (to.c.trade_sender_id == ctr.c.id) &
            (to.c.trade_post_id == trade_post_id)).join(ctn,
            (to.c.collection_send_id == ctn.c.id)).join(cbl,
            (ctn.c.collectible_id == cbl.c.id))

    select_stmt = (db.select(
        to.c.id.label("offer_id"),
        cbl.c.name.label("offer_collectible_name"),
        cbl.c.image.label("offer_collectible_img"),
        to.c.date_offered.label("offer_made_date"),
        ctr.c.username.label("trader_username"),
        ctr.c.profile_picture.label("trader_profile_img")
    ).select_from(join))

    offers = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    conn.close()

    return jsonify(offers)

# TODO: Error checking
def find_outgoing_offers(user_id):
    """Finds all outgoing offers the user has made

    Notes: id == sender_id

    Args:
        user_id (int): id of user who we want to find outgoing trade offers for
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers, collections, collectibles, and collectors table
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    join = db.join(to, ctr, 
            (to.c.trade_sender_id == ctr.c.id) &
            (to.c.trade_sender_id == user_id)).join(ctn,
            (to.c.collection_send_id == ctn.c.id)).join(cbl,
            (ctn.c.collectible_id == cbl.c.id))

    # Finds offers that the collector has made (finds sender information)
    select_stmt = (db.select(
        to.c.id.label("offer_id"),
        cbl.c.name.label("collectible_name"),
        cbl.c.image.label("ollectible_img"),
        to.c.date_offered.label("offer_made_date"),
        ctr.c.username.label("trader_username"),
        ctr.c.profile_picture.label("trader_profile_img"),
        to.c.trade_receiver_id.label("trade_receiver_id"),
        to.c.collection_receive_id.label("collection_receive_id")
    ).select_from(join))

    offers = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())

    # Loop through all the outgoing offers, and find the receiver information
    for offer in offers:
        receiver_id = offer.get("trade_receiver_id")
        find_stmt = db.select(ctr.c.username).where(ctr.c.id == receiver_id)
        receiver_name = conn.execute(find_stmt).fetchone()._asdict().get("name")
        offer["receiver_name"] = receiver_name
        
    conn.close()

    return jsonify(offers)

def accept_trade_offer(user_id, offer_id):
    """_summary_

    Args:
        user_id (_type_): _description_
        offer_id (_type_): _description_
    """
    return

# TODO: Error checking? Not sure if needed, since this is a helper and the main functions should handle errors already
def find_trade_offer_id(trade_post_id, sender_id, ctn_s_id, receiver_id, ctn_r_id):
    """_summary_

    Args:
        trade_post_id (int): id of the trade post
        sender_id (int): id of collector that is sending the trade
        ctn_s_id (int): collection id of collectible that sender wants to trade
        receiver_id (int): id of collector that is receiving the trade
        ctn_r_id (int): collection id of collectible that receiver has posted for trade
    
    Returns:
        int: the trade offer id
    
    Example Output:
        2
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers table
    to = db.Table("trade_offers", metadata, autoload_with=engine)

    select_stmt = db.select(to).where((to.c.trade_post_id == trade_post_id) &
                                      (to.c.trade_sender_id == sender_id) &
                                      (to.c.collection_send_id == ctn_s_id) &
                                      (to.c.trade_receiver_id == receiver_id) &
                                      (to.c.collection_receive_id == ctn_r_id))
    
    trade_offer_id = conn.execute(select_stmt).fetchone()._asdict().get("id")
    conn.close()

    return trade_offer_id

def find_num_trade_offers(trade_post_id):
    return
