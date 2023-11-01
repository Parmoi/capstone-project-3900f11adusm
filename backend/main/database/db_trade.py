import sqlalchemy as db
from flask import jsonify
import db_helpers
import db_manager as dbm
from error import OK, InputError, AccessError

"""
Preface:
    - trade_posts are posts that we find when we do searches. These are not
    for giving specific offers (like trading collectible "boat" for "fish"),
    but rather listing collectible "boat" as tradable for others to make offers for
    - trade_offers are created when we click on a trade_post item, and make
    an offer to the collector that lists it
"""


""" |------------------------------------|
    |     Functions for trade_posts      |
    |------------------------------------| """

# TODO: Error checking
# Note - would it better if we get trade_posts through collectible id?
def get_trade_posts(collectible_name):
    """Return all trade posts for a certain collectible

    Args:
        collectible_name (string): name of collectible we want to find trade
                                   posts for

    Returns:
        JSON, id: JSON holds the list of trade posts, int is the error code
    
    Example Output:
        {
            [
                {
                    "trade_post_id":1,
                    "post_title":"cool post!",
                    "post_description":"i made this randomly",
                    "post_images":["https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg", "https://google.com"],
                    "collector_id":1,
                    "username":"potato",
                    "profile_picture":"https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "address":"20 Cooper Street"
                },
                {
                    "trade_post_id":2,
                    "post_title":"another post!",
                    "post_description":"hhahahahahahahahhaha",
                    "post_images":["https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg", "https://google.com"],
                    "collector_id":2,
                    "username":"saitama",
                    "profile_picture":"https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "address":"74 Micro Avenue"
                }
            ]
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_listings, collections, collectibles and collectors table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    join = db.join(
        tp, ctn, tp.c.collection_id == ctn.c.id).join(cbl, 
            (ctn.c.collectible_id == cbl.c.id) &
            (cbl.c.name == collectible_name)).join(ctr,
            (tp.c.collector_id == ctr.c.id))

    select_stmt = (
        db.select(
            tp.c.id.label("trade_post_id"),
            ctr.c.id.label("collector_id"),
            ctr.c.username.label("username"),
            ctr.c.profile_picture.label("profile_picture"),
            ctr.c.address.label("address"),
            tp.c.post_title.label("post_title"),
            tp.c.post_description.label("post_description"),
            tp.c.post_images.label("post_images")
        ).select_from(join)
    )

    trade_posts = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    conn.close()

    return jsonify(trade_posts), OK

# TODO: Error checking (valid collection_id, valid collector_id, valid title/desc/imgs)
def insert_trade_post(collector_id, collection_id, post_title, post_desc, post_imgs):
    """Takes a collectible we have in our collection, and puts it up for trade

    Args:
        collector_id (int): id of collector that wants to list something for trade
        collection_id (int): the collection id of the collectible we want to trade
        post_title (string): title of the trade post
        post_desc (string): description of the trade post
        post_imgs ([string]): list of string of the image urls for that post

    Returns:
        JSON, id: JSON of our trade_post id, and id of the error code
    
    Example Output:
        {"trade_post_id": 1}, 200
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_listings table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)

    # Since SQL can't store lists, we must convert img list to delimited string
    delimited_post_imgs = ",".join(post_imgs)

    insert_stmt = db.insert(tp).values(
        {
            "collector_id": collector_id,
            "collection_id": collection_id,
            "post_title": post_title,
            "post_description": post_desc,
            "post_images": delimited_post_imgs
        }
    )
    conn.execute(insert_stmt)
    conn.close()

    # Find the id of the trade_post associated with the new entry
    trade_post_id = find_trade_post(collector_id, collection_id)

    return jsonify({"trade_post_id": trade_post_id}), OK

# TODO: Error checking
def remove_trade_post(collector_id, collection_id):
    """Remove the trade post associated with the collector and their posted collectible

    Args:
        collector_id (int): id of collector
        collection_id (int): id of collectible in their collection they want to 
        remove from posts

    Returns:
        JSON, id: JSON of our removed trade_post id, and id of the error code
    
    Example Output:
        {"trade_post_id": 1}, 200
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_listings table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)

    # Find id associated with trade listing we want to remove
    trade_post_id = find_trade_post(collector_id, collection_id)

    # Delete the matching trade_listing row
    delete_stmt = db.delete(tp).where(
        (tp.c.collector_id == collector_id) &
        (tp.c.collection_id == collection_id))
    conn.execute(delete_stmt)
    conn.close()

    return jsonify({"trade_post_id": trade_post_id}), OK


# Error checking not necessary, as this should be called after the other functions already do a check
def find_trade_post(collector_id, collection_id):
    """Finds the trade_post id associated with the collector_id and collection_id

    Args:
        collector_id (int): id of the collector
        collection_id (int): id of the collectible within the collection

    Returns:
        int: trade post id
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_listings table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    
    select_stmt = db.select(tp).where(
        (tp.c.collector_id == collector_id) &
        (tp.c.collection_id == collection_id))

    # Find and return the corresponding trade_post id
    tp_id = conn.execute(select_stmt).fetchone()._asdict().get("id")
    conn.close()

    return tp_id

""" |------------------------------------|
    |     Functions for trade_offers     |
    |------------------------------------| """

def send_trade_offer(sender_id, trade_post_id, ):
    return

"""
Note:
- Functions we might want:
    - Find outgoing trades (where id == sender_id)
    - Find incoming trades (where id == receiver_id)
"""