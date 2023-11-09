import sqlalchemy as db
from flask import jsonify
import db_helpers
import db_manager as dbm
from error import OK, InputError, AccessError

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
            "collection_receive_id": ctn_r_id
        })
    conn.execute(insert_stmt)
    conn.close()

    # Find the id associated with the trade offer
    trade_offer_id = find_trade_offer(trade_post_id, sender_id, ctn_s_id, receiver_id, ctn_r_id)
    
    return jsonify({"trade_offer_id": trade_offer_id}), OK

# TODO: Error checking
def find_incoming_offers(user_id):
    """Finds all incoming offers for a user

    Notes: id == receiver_id

    Args:
        user_id (int): id of user we want to find offers for
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_offers, collections and collectibles table
    to = db.Table("trade_offers", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)

    
    

    return

# TODO: Error checking
def find_outgoing_offers(user_id):
    """Finds all outgoing offers the user has made

    Notes: id == sender_id

    Args:
        user_id (int): id of user who we want to find outgoing trade offers for
    """
    return

def accept_trade_offer(user_id, offer_id):
    """_summary_

    Args:
        user_id (_type_): _description_
        offer_id (_type_): _description_
    """
    return

# TODO: Error checking? Not sure if needed, since this is a helper and the main functions should handle errors already
def find_trade_offer(trade_post_id, sender_id, ctn_s_id, receiver_id, ctn_r_id):
    return


"""
Questions:
- For the trade offers, what does the frontend want returned?
    - For outgoing: just return information of user we sent offer to?
    - For incoming: just return information of user who sent us offer?
"""