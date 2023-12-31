from datetime import date
from flask import jsonify
import sqlalchemy as db

from error import OK
import db_collections, db_exchangehistory, db_helpers
import db_manager as dbm, db_past_tradeoffers


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
            "date_offered": date.today(),
            "date_updated": date.today()
        })
    conn.execute(insert_stmt)
    conn.close()

    # Find the id associated with the trade offer
    trade_offer_id = find_trade_offer_id(tp_id, send_id, ctn_s_id)
    
    return jsonify({"trade_offer_id": trade_offer_id}), OK


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
                    "collectible_id": 2,
                    "offer_collectible_img": "https://robohash.org/voluptatemetipsum.png?size=50x50&set=set1",
                    "offer_collectible_name": "Phascogale calura",
                    "offer_id": 1,
                    "offer_made_date": "10/11/2023",
                    "offer_message": "I would like to TAKE THIS!",
                    "trader_id": 20,
                    "trader_profile_img": "https://robohash.org/cumqueaccusamusvoluptas.png?size=50x50&set=set1",
                    "trader_name": "uamar"
                },
                {
                    "collectible_id": 4
                    "offer_collectible_img": "https://robohash.org/estcumquedebitis.png?size=50x50&set=set1",
                    "offer_collectible_name": "Ictonyx striatus"
                    "offer_id": 2,
                    "offer_made_date": "10/11/2023",
                    "offer_message": "I would like to trade!",
                    "trader_id": 25,
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
        cbl.c.id.label("collectible_id"),
        cbl.c.name.label("offer_collectible_name"),
        cbl.c.image.label("offer_collectible_img"),
        to.c.date_offered.label("offer_made_date"),
        to.c.offer_message.label("offer_message"),
        ctr.c.id.label("trader_id"),
        ctr.c.username.label("trader_name"),
        ctr.c.profile_picture.label("trader_profile_img")
    ).select_from(join))

    offers = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    conn.close()

    return jsonify(offers)


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
                    "collectible_r_id": 5,
                    "collectible_r_name": "Iguana iguana",
                    "collectible_r_img": "https://robohash.org/similiquenemoaut.png?size=50x50&set=set1",
                    "collectible_s_id": 2,
                    "collectible_s_name": "Phascogale calura",
                    "collectible_s_img": "https://robohash.org/voluptatemetipsum.png?size=50x50&set=set1",
                    "offer_status": "SENT",
                    "date_offer_sent": "11/11/2023",
                    "date_updated": "14/11/2023",
                    "trader_collector_id": 3,
                    "trader_name": "uso",
                    "trader_profile_picture": "google.com."
                },
                {
                    "collectible_r_id": 2,
                    "collectible_r_name": "Iguana iguana",
                    "collectible_r_img": "https://robohash.org/similiquenemoaut.png?size=50x50&set=set1",
                    "collectible_s_id": 3,
                    "collectible_s_name": "Phascogale calura",
                    "collectible_s_img": "https://robohash.org/voluptatemetipsum.png?size=50x50&set=set1",
                    "offer_status": "DECLINED",
                    "date_offer_sent": "13/11/2023",
                    "date_updated": "14/11/2023",
                    "trader_collector_id": 1,
                    "trader_name": "bob",
                    "trader_profile_picture": "https://robohash.org/utomniseos.png?size=50x50&set=set1"
                }
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
        cbl.c.id.label("collectible_s_id"),
        cbl.c.name.label("collectible_s_name"),
        cbl.c.image.label("collectible_s_img"),
        to.c.date_offered.label("date_offer_sent"),
        to.c.offer_status.label("offer_status"),
        to.c.date_updated.label("date_updated"),
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
            cbl.c.id.label("collectible_r_id"),
            cbl.c.name.label("collectible_r_name"),
            cbl.c.image.label("collectible_r_img"),
            ctr.c.id.label("trader_collector_id"),
            ctr.c.username.label("trader_name"),
            ctr.c.profile_picture.label("trade_profile_img")
        )).select_from(new_join)
        details_dict = conn.execute(find_stmt).fetchone()._asdict()
        offer.update(details_dict)
        offer.pop("trade_post_id")
        offer.pop("offer_id")
    # Finds and appends all offers that have been accepted/declined in the past
    offer_list = offers + db_past_tradeoffers.find_past_outgoing_offers(
        user_id, engine, conn, metadata)

    conn.close()
    return jsonify(offer_list), OK


def accept_trade_offer(offer_id):
    """Function to accept a trade offer

    Args:
        offer_id (int): id of the offer we want to accept
    
    Returns:
        JSON, int: JSON of offer_id, int of success/error code
    
    Example Output:
        {"offer_id": 2}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_posts, trade_offers, and trade_post_images tables
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    tp_img = db.Table("trade_post_images", metadata, autoload_with=engine)
    
    # Change offer status from "SENT" to "ACCEPTED"
    update_stmt = db.update(to).where(to.c.id == offer_id).values({
        "offer_status": "ACCEPTED",
        "date_updated": date.today()
    })

    conn.execute(update_stmt)

    # Save our trade post - trade offer information, and find the trade post id
    tp_to_info = to_tp_info(offer_id, engine, conn, metadata)
    trade_post_id = tp_to_info.get("trade_post_id")

    # This will move our trade offer to past_trade_offers table, and delete the trade offer
    db_past_tradeoffers.move_to_past(offer_id, engine, conn, metadata)
    
    # For all the other trades, automatically set them to "DECLINED"
    offers_update_stmt = db.update(to).where(
        to.c.trade_post_id == trade_post_id).values(offer_status = "DECLINED")
    conn.execute(offers_update_stmt)

    # Find the id of the remaining trade offers, and send them to "past_trade_offers" table
    find_remaining_offers_stmt = db.select(to).where(to.c.trade_post_id == trade_post_id)
    remaining_offers = conn.execute(find_remaining_offers_stmt).fetchall()
    for offer in remaining_offers:
        curr_offer_id = offer._asdict().get("id")
        db_past_tradeoffers.move_to_past(curr_offer_id, engine, conn, metadata)

    # Delete trade post images associated with the trade post
    post_img_delete_stmt = db.delete(tp_img).where(
        tp_img.c.trade_post_id == trade_post_id)
    conn.execute(post_img_delete_stmt)

    # Delete the trade post
    post_delete_stmt = db.delete(tp).where(tp.c.id == trade_post_id)
    conn.execute(post_delete_stmt)

    # Get the id's of traders, and the traders' collection_id
    receiver_id = tp_to_info.get("receiver_id")
    collection_r_id = tp_to_info.get("collection_r_id")
    sender_id = tp_to_info.get("sender_id")
    collection_s_id = tp_to_info.get("collection_s_id")

    # Adds the accepted trade offer into the exchange history table
    db_exchangehistory.add_exhange_history(tp_to_info, engine, conn, metadata)
    
    # Moves collectible from sender to receiver
    db_collections.move_collectible(sender_id, receiver_id, collection_s_id)

    # Moves the collectible from receiver to sender
    db_collections.move_collectible(receiver_id, sender_id, collection_r_id)

    conn.close()

    return jsonify({"offer_id": offer_id}), OK


def decline_trade_offer(offer_id):
    """Function to decline a trade offer

    Args:
        offer_id (int): id of the trade offer that we want to decline

    Returns:
        JSON, int: JSON of id of declined offer, int of success/error code
    
    Example Output:
        {"offer_id": 2}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers table
    to = db.Table("trade_offers", metadata, autoload_with=engine)

    # Change offer status from "SENT" to "DECLINED"
    update_stmt = db.update(to).where(to.c.id == offer_id).values({
        "offer_status": "DECLINED",
        "date_updated": date.today()
    })
    conn.execute(update_stmt)

    # Will move our trade offer from trade_offers to past_trade_offers table
    db_past_tradeoffers.move_to_past(offer_id, engine, conn, metadata)

    return jsonify({"offer_id": offer_id}), OK

""" |------------------------------------|
    |  Helper Functions for tradeoffers  |
    |------------------------------------| """


def find_trade_offer_id(trade_post_id, sender_id, ctn_s_id):
    """Find trade offer id from the trade post, sender id and sent collection id

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

def to_tp_info(offer_id, engine, conn, metadata):
    """Returns the trade offer and the corresponding trade post information

    Notes:
        engine, conn, metadata included in arguments (db connectors)
    
    Args:
        offer_id (int): id of trade offer we want to find information for
    
    Returns:
        dictionary: holds information of trade_offer and corresponding trade_post

    Example Output:
        {
            "trade_post_id": 20,
            "receiver_id": 1,
            "collection_r_id": 501,
            "sender_id": 2
            "collection_s_id": 502,
            "offer_message": "random msg!",
            "offer_image": "google.com",
            "offer_status": "SENT",
            "date_offered": "12/11/2023",
            "date_updated": "25/11/2023"
        }
    """
    # Loads in the trade_offers, collections, collectibles, and collectors table
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    tp = db.Table("trade_posts", metadata, autoload_with=engine)

    join = db.join(to, tp,
        (to.c.trade_post_id == tp.c.id) & (to.c.id == offer_id))
    
    select_stmt = (db.select(
        tp.c.id.label("trade_post_id"),
        tp.c.collector_id.label("receiver_id"),
        tp.c.collection_id.label("collection_r_id"),
        to.c.trade_sender_id.label("sender_id"),
        to.c.collection_send_id.label("collection_s_id"),
        to.c.offer_message.label("offer_message"),
        to.c.offer_image.label("offer_image"),
        to.c.offer_status.label("offer_status"),
        to.c.date_offered.label("date_offered"),
        to.c.date_updated.label("date_updated"),
    )).select_from(join)

    tp_to_info = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())[0]

    return tp_to_info