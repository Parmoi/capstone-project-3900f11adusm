import sqlalchemy as db
from flask import jsonify
import db_helpers
import db_manager as dbm
import db_collections
from error import OK, InputError, AccessError
from datetime import date

# TODO: Error checking
def register_trade_offer(tp_id, send_id, ctn_s_id, offer_msg, offer_img):
    """Generates a new trade offer for a certain trade_post

    Args:
        tp_id (int): id of the trade post that we making an offer for
        send_id (int): id of collector that is sending the trade offer
        ctn_s_id (int): (collection_send_id) id of collectible in collection to send
    
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
            "trade_post_id": tp_id,
            "trade_sender_id": send_id,
            "collection_send_id": ctn_s_id,
            "offer_message": offer_msg,
            "offer_image": offer_img,
            "offer_status": "SENT",
            "date_offered": date.today()
        })
    conn.execute(insert_stmt)
    conn.close()

    # Find the id associated with the trade offer
    trade_offer_id = find_trade_offer_id(tp_id, send_id, ctn_s_id)
    
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
                    "offer_message": "I would like to TAKE THIS!",
                    "trader_profile_img": "https://robohash.org/cumqueaccusamusvoluptas.png?size=50x50&set=set1",
                    "trader_name": "uamar"
                },
                {
                    "offer_collectible_img": "https://robohash.org/estcumquedebitis.png?size=50x50&set=set1",
                    "offer_collectible_name": "Ictonyx striatus"
                    "offer_id": 2,
                    "offer_made_date": "10/11/2023",
                    "offer_message": "I would like to trade!",
                    "trader_profile_img": "https://robohash.org/nesciuntculpaat.png?size=50x50&set=set1",
                    "trader_name": "szhang"
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
            (to.c.trade_post_id == trade_post_id) &
            (to.c.offer_status != "DECLINED")).join(ctn,
            (to.c.collection_send_id == ctn.c.id)).join(cbl,
            (ctn.c.collectible_id == cbl.c.id))

    select_stmt = (db.select(
        to.c.id.label("offer_id"),
        cbl.c.name.label("offer_collectible_name"),
        cbl.c.image.label("offer_collectible_img"),
        to.c.date_offered.label("offer_made_date"),
        to.c.offer_message.label("offer_message"),
        ctr.c.username.label("trader_name"),
        ctr.c.profile_picture.label("trader_profile_img")
    ).select_from(join))

    offers = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    conn.close()

    return jsonify(offers)

# TODO: Error checking (empty lists?)
def find_outgoing_offers(user_id):
    """Finds all outgoing offers the user has made

    Notes:
        id == sender_id

    Args:
        user_id (int): id of user who we want to find outgoing trade offers for
    
    Returns:
        JSON, int: JSON of list of offers the user has sent, int of error code
    
    Example Output:
        {
            [
                {
                    "offer_id": 1,
                    "collectible_s_name": "Phascogale calura",
                    "collectible_s_img": "https://robohash.org/voluptatemetipsum.png?size=50x50&set=set1",
                    "collectible_r_name": "Iguana iguana",
                    "collectible_r_img": "https://robohash.org/similiquenemoaut.png?size=50x50&set=set1",
                    "offer_status": "SENT",
                    "date_offer_sent": "11/11/2023",
                    "trader_name": "uso",
                    "trade_post_id": 1
                },
                ...
            ]
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers, collections, collectibles, and collectors table
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    join = db.join(to, ctn,
            (to.c.collection_send_id == ctn.c.id) &
            (to.c.trade_sender_id == user_id)).join(cbl,
            (ctn.c.collectible_id == cbl.c.id))

    # Finds offers that the collector has made
    select_stmt = (db.select(
        to.c.id.label("offer_id"),
        cbl.c.name.label("collectible_s_name"), # Collectible send name
        cbl.c.image.label("collectible_s_img"), # Collectible send image
        to.c.date_offered.label("date_offer_sent"),
        to.c.offer_status.label("offer_status"),
        to.c.trade_post_id.label("trade_post_id")
    ).select_from(join))

    offers = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())

    # Loop through all the outgoing offers, and find the poster's information
    for offer in offers:
        tp_id = offer.get("trade_post_id")
        new_join = db.join(tp, ctr, 
                    (tp.c.id == tp_id) &
                    (tp.c.collector_id == ctr.c.id)).join(ctn,
                    (tp.c.collection_id == ctn.c.id)).join(cbl,
                    (ctn.c.collectible_id == cbl.c.id))
        find_stmt = (db.select(
            cbl.c.name.label("collectible_r_name"),
            cbl.c.image.label("collectible_r_img"),
            ctr.c.username.label("trader_name")
        )).select_from(new_join)
        details_dict = conn.execute(find_stmt).fetchone()._asdict()
        offer.update({
            "collectible_r_name": details_dict.get("collectible_r_name"),
            "collectible_r_img": details_dict.get("collectible_r_img"),
            "trader_name": details_dict.get("trader_name"),
        })
        
    conn.close()

    return jsonify(offers), OK

# TODO: Error checking
def accept_trade_offer(offer_id):
    """_summary_

    Notes:
        - Change offer status from "SENT" to "ACCEPTED"                 [DONE]
        - Remove collectible from sender's collection                   
        - Remove collectible from receiver's collection
        - Add collectible to sender's collection
        - Add collectible to receiver's collection
        - Add entry to exchange history
        - Archive system???? (so we don't completely remove posts from view) -> 
            - Add to trade_post: "post_status" = "CLOSED"/"OPEN"
            - The thing is we can delete trade_posts, but this will cause us problem (when we try to reference it later)
            - E.g. find_outgoing_offers uses trade_post information

    Args:
        user_id (_type_): _description_
        offer_id (_type_): _description_
    
    Returns:
        ...
    
    Example Output:
        ...
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_posts, trade_offers, collections and collectibles table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)

    # Change offer status from "SENT" to "ACCEPTED"
    update_stmt = db.update(to).where(to.c.id == offer_id).values(offer_status = "ACCEPTED")
    conn.execute(update_stmt)
    
    join = db.join(tp, to, (to.c.trade_post_id == tp.c.id) & (to.c.id == offer_id))
    select_stmt = (db.select(
        tp.c.collector_id.label("receiver_id"),
        tp.c.collection_id.label("collection_r_id"),
        to.c.trade_sender_id.label("sender_id"),
        to.c.collection_send_id.label("collection_s_id")
    ).select_from(join))

    trade_offer_info = conn.execute(select_stmt).fetchone()._asdict()

    receiver_id = trade_offer_info.get("receiver_id")
    collection_r_id = trade_offer_info.get("collection_r_id")
    sender_id = trade_offer_info.get("sender_id")
    collection_s_id = trade_offer_info.get("collection_s_id")

    # Moves the collectible from sender to receiver
    db_collections.move_collectible(sender_id, receiver_id, collection_s_id)

    # Moves the collectible from receiver to sender
    db_collections.move_collectible(receiver_id, sender_id, collection_r_id)
    
    conn.close()

    return jsonify({"offer_id": offer_id}), OK

# TODO: Error checking (empty lists?)
def decline_trade_offer(offer_id):
    """Function to decline a trade offer

    Args:
        offer_id (int): id of the trade offer that we want to decline

    Returns:
        JSON: JSON of the id of the trade offer that was declined
    
    Example Output:
        2
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers table
    to = db.Table("trade_offers", metadata, autoload_with=engine)

    # Change offer status from "SENT" to "DECLINED"
    update_stmt = db.update(to).where(to.c.id == offer_id).values(offer_status = "DECLINED")
    conn.execute(update_stmt)
    conn.close()

    return jsonify({"offer_id": offer_id}), OK

# TODO: Error checking? Not sure if needed, since this is a helper and the main functions should handle errors already
def find_trade_offer_id(trade_post_id, sender_id, ctn_s_id):
    """_summary_

    Args:
        trade_post_id (int): id of the trade post
        sender_id (int): id of collector that is sending the trade
        ctn_s_id (int): collection id of collectible that sender wants to trade
    
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
                                      (to.c.collection_send_id == ctn_s_id))
    
    trade_offer_id = conn.execute(select_stmt).fetchone()._asdict().get("id")
    conn.close()

    return trade_offer_id

