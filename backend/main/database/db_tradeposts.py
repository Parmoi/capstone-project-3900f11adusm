import sqlalchemy as db
from flask import jsonify
import db_helpers
import db_manager as dbm
from error import OK, InputError, AccessError
from datetime import date

"""
Preface:
    - trade_posts are posts that we find when we do searches. These are not
    for giving specific offers (like trading collectible "boat" for "fish"),
    but rather listing collectible "boat" as tradable for others to make offers for
    - trade_offers are created when we click on a trade_post item, and make
    an offer to the collector that lists it
"""

# TODO: Error checking
def get_trade_posts(collectible_id):
    """Returns all trade posts for a certain collectible

    Notes:
        currently, this API call is actually called "buylist", and is called by
        `get_buylist()`

    Args:
        collectible_id (int): id of collectible we want to find trade posts for

    Returns:
        JSON, int: JSON holds list of trade posts, int is the error code
    
    Example Output:
        {
            [
                {
                    "trade_post_id": 1,
                    "collection_id": 501,
                    "image": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "collectible_name": "iguana",
                    "trader_name": "Mr Bean",
                    "trader_profile_img": ""https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "location": "Kensington, NSW"
                },
                {
                    "trade_post_id": 2,
                    "collection_id": 505,
                    "image": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "collectible_name": "iguana",
                    "trader_name": "Peter Pan",
                    "trader_profile_img": ""https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "location": "Central, NSW"
                }
            ]
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_posts, collections, collectibles and collectors table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    join = db.join(tp, ctn, 
        (tp.c.collection_id == ctn.c.id)).join(cbl, 
        (cbl.c.id == collectible_id) &
        (ctn.c.collectible_id == cbl.c.id)).join(ctr,
        (tp.c.collector_id == ctr.c.id))

    select_stmt = (
        db.select(
            ctn.c.id.label("collection_id"),
            cbl.c.image.label("image"),
            cbl.c.name.label("collectible_name"),
            ctr.c.username.label("trader_name"),
            ctr.c.profile_picture.label("trader_profile_img"),
            ctr.c.address.label("location"),
            tp.c.id.label("trade_post_id")
        ).select_from(join)
    )
    trade_posts = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    conn.close()

    return jsonify(trade_posts), OK
    
# TODO: Error checking
def get_current_trade_posts(collector_id):
    """Finds the trade posts that the collector has posted

    Args:
        collector_id (int): id of the collector

    Returns:
        JSON, int: JSON of collector's trade posts, int of error code

    Example Output:
        [
            {
                "trade_post_id": 1,
                "trader_collection_id": 501,
                "trade_collectible_id": 1,
                "trader_collectible_name": "Iguana iguana",
                "trader_collectible_img": "https://robohash.org/similiquenemoaut.png?size=50x50&set=set1",
                "trade_post_date": "10/11/2023",
                "offers_received": 2,
            },
            {
                "trade_post_id": 2,
                "trader_collection_id": 503,
                "trade_collectible_id": 2,
                "trader_collectible_name": "Superman (Holo)",
                "trader_collectible_img": "https://robohash.org/similiquenemoaut.png?size=50x50&set=set1",
                "trade_post_date": "05/11/2023",
                "offers_received": 4,
            },
        ]
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_posts, collections, collectibles and collectors table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)
    to = db.Table("trade_offers", metadata, autoload_with=engine)

    join = db.join(tp, ctn, 
        (tp.c.collection_id == ctn.c.id) &
        (tp.c.collector_id == collector_id)).join(cbl, 
        (ctn.c.collectible_id == cbl.c.id)).join(ctr,
        (tp.c.collector_id == ctr.c.id)).join(to,
        (to.c.trade_post_id == tp.c.id) &
        (to.c.offer_status == "SENT"), isouter=True)

    select_stmt = (
        db.select(
            tp.c.id.label("trade_post_id"),
            ctn.c.id.label("trader_collection_id"),
            cbl.c.id.label("trader_collectible_id"),
            cbl.c.name.label("trader_collectible_name"),
            tp.c.post_date.label("trade_post_date"),
            cbl.c.image.label("trader_collectible_img"),
            db.func.count(to.c.id).label("offers_received")
        ).group_by(
            tp.c.id, ctn.c.id, cbl.c.id, cbl.c.name, tp.c.post_date, cbl.c.image
        ).select_from(join)
    )

    trade_posts = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())
    conn.close()

    return jsonify(trade_posts), OK

# TODO: Error checking
def get_trade_post_info(trade_post_id):
    """Gets the information for a trade post

    Args:
        trade_post_id (int): id of the trade post we want information for

    Returns:
        JSON, int: JSON holds trade post information, int of error code

    Example Output:
        {
            "post_title":"random post!",
            "post_description":"random desc!",
            "post_created":"08/11/2023",
            "post_images":[
                {
                    "caption":"Bart with skateboard.",
                    "image":"https://tse1.mm.bing.net/th?id=OIP.S9zFPgPbF0zJ4OXQkU675AHaHC&pid=Api",
                    "name":"1"
                },
                {
                    "caption":"Stuffed bart.",
                    "image":"https://tse1.mm.bing.net/th?id=OIP.AIizpaWw4l8TtY5fWj66RgHaGr&pid=Api",
                    "name":"2"
                }],
            "post_trader":"uso",
            "trader_avatar":"https://robohash.org/utomniseos.png?size=50x50&set=set1",
            "trader_location":"696 Londonderry Avenue",
            "trader_id":"1"
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_posts, collections, collectibles and collectors table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    ctn = db.Table("collections", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    # Load in the trade_post_images table
    tp_imgs = db.Table("trade_post_images", metadata, autoload_with=engine)

    join = db.join(tp, ctn,
        (tp.c.collection_id == ctn.c.id) &
        (tp.c.id == trade_post_id)).join(cbl,
        (ctn.c.collectible_id == cbl.c.id)).join(ctr,
        (tp.c.collector_id == ctr.c.id))

    select_stmt = (
        db.select(
            tp.c.post_title.label("post_title"),
            tp.c.post_date.label("post_created"),
            tp.c.post_description.label("post_description"),
            ctr.c.username.label("post_trader"),
            ctr.c.profile_picture.label("trader_avatar"),
            ctr.c.address.label("trader_location")
        ).select_from(join)
    )

    # TODO: TEST
    post_info = db_helpers.rows_to_list(conn.execute(select_stmt).fetchall())[0]

    img_select_stmt = (
        db.select(
            tp_imgs.c.name.label("name"),
            tp_imgs.c.caption.label("caption"),
            tp_imgs.c.image_url.label("image")
        ).where(tp_imgs.c.trade_post_id == trade_post_id)
    )
    # Finds image list and adds it to the dictionary
    image_list = db_helpers.rows_to_list(conn.execute(img_select_stmt).fetchall())
    post_info["post_images"] = image_list
    conn.close()

    return jsonify(post_info), OK


# TODO: Error checking (valid collection_id, valid collector_id, valid title/desc/imgs)
def insert_trade_post(collector_id, collection_id, post_title, post_desc, post_imgs):
    """Takes a collectible we have in our collection, and puts it up for trade

    Notes:
        post_imgs are stored in their own table

    Args:
        collector_id (int): id of collector that wants to list something for trade
        collection_id (int): the collection id of the collectible we want to trade
        post_title (string): title of the trade post
        post_desc (string): description of the trade post
        post_imgs ([dictionary]): list of dicts for the images of the post

    Returns:
        JSON, id: JSON of our trade_post id, and id of the error code
    
    Example Output:
        {"trade_post_id": 1}, 200
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the trade_posts and trade_post_images table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    tp_imgs = db.Table("trade_post_images", metadata, autoload_with=engine)

    insert_stmt = db.insert(tp).values(
        {
            "collector_id": collector_id,
            "collection_id": collection_id,
            "post_title": post_title,
            "post_description": post_desc,
            "post_date": date.today()
        }
    )
    conn.execute(insert_stmt)

    # Find the id of the trade_post associated with the new entry
    trade_post_id = find_trade_post(collector_id, collection_id)

    # Add the images to the trade_post_images table
    for image_dict in post_imgs:
        insert_img_stmt = db.insert(tp_imgs).values(
            {
                "trade_post_id": trade_post_id,
                "name": image_dict.get("name"),
                "caption": image_dict.get("caption"),
                "image_url": image_dict.get("image")
            }
        )
        conn.execute(insert_img_stmt)
    conn.close()

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

    # Loads in the trade_posts and trade_post_images table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    tp_imgs = db.Table("trade_post_images", metadata, autoload_with=engine)

    # Find id associated with trade listing we want to remove
    trade_post_id = find_trade_post(collector_id, collection_id)

    # Delete the matching trade_post row
    delete_stmt = db.delete(tp).where(
        (tp.c.collector_id == collector_id) &
        (tp.c.collection_id == collection_id))
    conn.execute(delete_stmt)

    # Remove the images from the trade_post_images table
    delete_img_stmt = db.delete(tp_imgs).where(tp_imgs.c.trade_post_id == trade_post_id)
    conn.execute(delete_img_stmt)
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

    # Loads in the trade_posts table
    tp = db.Table("trade_posts", metadata, autoload_with=engine)
    
    select_stmt = db.select(tp).where(
        (tp.c.collector_id == collector_id) &
        (tp.c.collection_id == collection_id))

    # Find and return the corresponding trade_post id
    tp_id = conn.execute(select_stmt).fetchone()._asdict().get("id")
    conn.close()

    return tp_id

