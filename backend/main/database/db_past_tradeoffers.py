from datetime import datetime
import sqlalchemy as db

import db_helpers, db_tradeoffers, db_collections


def find_past_outgoing_offers(user_id, engine, conn, metadata):
    """Finds all past offers that the user has made (since ACCCEPTED/DECLINED offers are deleted)

    Notes:
        engine, conn, metadata included in arguments (db connection helpers)

    Args:
        user_id (int): id of collector we want to find past outgoing offers for

    Returns:
        [dictionary]: list of dictionaries containing offer information
    
    Example Output:
        [
            {
                "collectible_r_img": "https://robohash.org/similiquenemoaut.png?size=50x50&set=set1",
                "collectible_r_name": "Iguana iguana",
                "collectible_receive_id": 2,
                "collectible_s_id": 3
                "collectible_s_img": "https://robohash.org/voluptatemetipsum.png?size=50x50&set=set1",
                "collectible_s_name": "Phascogale calura",
                "date_offer_sent": "13/11/2023",
                "date_updated": "20/11/2023",
                "offer_status": "DECLINED",
                "trade_receiver_id": 1,
                "trader_name": "uso",
                "trader_profile_img": "https://robohash.org/utomniseos.png?size=50x50&set=set1"
            },
        ]
    """
    # Loads in the past_trade_offers, collectors and collectibles table
    past_to = db.Table("past_trade_offers", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)

    # First we find past posts where user has sent offers
    join = db.join(past_to, cbl,
        (past_to.c.trade_sender_id == user_id) & 
        (past_to.c.collectible_send_id == cbl.c.id)).join(ctr,
        (past_to.c.trade_receiver_id == ctr.c.id))

    select_stmt = (db.select(
        cbl.c.id.label("collectible_s_id"),
        cbl.c.name.label("collectible_s_name"),
        cbl.c.image.label("collectible_s_img"),
        past_to.c.offer_status.label("offer_status"),
        past_to.c.date_offered.label("date_offer_sent"),
        past_to.c.date_updated.label("date_updated"),
        past_to.c.trade_receiver_id.label("trade_receiver_id"),
        past_to.c.collectible_receive_id.label("collectible_receive_id"),
    ).select_from(join))

    offers = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    
    for offer in offers:
        trade_receiver_id = offer.get("trade_receiver_id")
        collectible_receive_id = offer.get("collectible_receive_id")
        
        trader_select_stmt = (db.select(
            ctr.c.id.label("trader_collector_id"),
            ctr.c.username.label("trader_name"),
            ctr.c.profile_picture.label("trader_profile_img")
        )).where(ctr.c.id == trade_receiver_id)
        trader_info = conn.execute(trader_select_stmt).fetchone()._asdict()
        offer.update(trader_info)

        collectible_select_stmt = (db.select(
            cbl.c.id.label("collectible_r_id"),
            cbl.c.name.label("collectible_r_name"),
            cbl.c.image.label("collectible_r_img")
        )).where(cbl.c.id == collectible_receive_id)
        collectible_info = conn.execute(collectible_select_stmt).fetchone()._asdict()
        offer.update(collectible_info)
    
    return offers


def move_to_past(offer_id, engine, conn, metadata):
    """Moves an offer from the trade_offers table to the past_trade_offers table

    Args:
        offer_id (int): id of the offer we want to move
        engine, conn, metadata: just for connection to db

    Returns:
        dictionary: message of success/error

    Example Output:
        {"msg": "Offer 2 has been move from trade_offers to past_trade_offers!"}
    """
    # Loads in the trade_offers and past_trade_offers table
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    past_to = db.Table("past_trade_offers", metadata, autoload_with=engine)

    # Find trade_post and trade_offer information
    tp_to_info = db_tradeoffers.to_tp_info(offer_id, engine, conn, metadata)

    # Convert collection ids to collectible ids
    collection_s_id = tp_to_info.get("collection_s_id")
    collectible_s_id = db_collections.get_collectible_id(collection_s_id)
    collection_r_id = tp_to_info.get("collection_r_id")
    collectible_r_id = db_collections.get_collectible_id(collection_r_id)

    # Convert date_offered and date_updated from string to a Date object
    date_offered_obj = datetime.strptime(tp_to_info.get("date_offered"), "%d/%m/%Y").date()
    date_updated_obj = datetime.strptime(tp_to_info.get("date_updated"), "%d/%m/%Y").date()

    # Copies the trade offer to the past_trade_offers table
    insert_stmt = db.insert(past_to).values(
        {
            "trade_sender_id": tp_to_info.get("sender_id"),
            "collectible_send_id": collectible_s_id,
            "trade_receiver_id": tp_to_info.get("receiver_id"),
            "collectible_receive_id": collectible_r_id,
            "date_offered": date_offered_obj,
            "date_updated": date_updated_obj,
            "offer_status": tp_to_info.get("offer_status"),
        })
    conn.execute(insert_stmt)

    # Delete the trade offer from the trade_offer table
    delete_stmt = db.delete(to).where(to.c.id == offer_id)
    conn.execute(delete_stmt)

    return {"msg": f"Offer {offer_id} has been move from trade_offers to past_trade_offers!"}