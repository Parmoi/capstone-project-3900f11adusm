import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_collectibles
import db_helpers
from error import OK, InputError, AccessError
from datetime import date

""" |------------------------------------|
    |      Functions for wantlist        |
    |------------------------------------| """

# TODO: Error checking (valid user)
def get_wantlist(user_id):
    """Return the wantlist of the user with user_id

    Args:
        user_id (int): id of the user whose wantlist we want to find

    Returns:
        [dictionary]: list of dictionary objects with collectible details
    
    Example Output:
    {
        "msg": "Wantlist has been successfully delivered!",
        "wantlist": {
            "collectible_name": "random",
            "collectible_image": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
            "campaign_name": "cool_superhero",
            "date_added": ????
        }
    }
    """
    engine, conn, metadata = dbm.db_connect()

    # Load in the wantlist, campaign and collectible tables
    want = db.Table("wantlist", metadata, autoload_with=engine)
    coll = db.Table("collectibles", metadata, autoload_with=engine)
    camp = db.Table("campaigns", metadata, autoload_with=engine)

    # Join the tables
    join = db.join(want, coll, 
                   (want.c.collector_id == user_id) & 
                   (want.c.collectible_id == coll.collectible_id)
                   ).join(camp, coll.c.campaign_id == camp.c.id)
    
    search_stmt = (
        db.select(
            coll.c.name.label("collectible_name"),
            coll.c.image.label("collectible_image"),
            camp.c.name.label("campaign_name"),
            want.c.date_added.label("date_added")
        )
        .select_from(join)
    )

    wantlist = db_helpers.rows_to_list(conn.execute(search_stmt).fetchall())
    conn.close()

    return jsonify(
        {
        "msg": "Wantlist has been successfully delivered!",
        "wantlist": wantlist
        }
    ), OK


# TODO: Error checking (valid user, valid collectible name)
def insert_wantlist(collector_id, collectible_name):
    """Function to insert a collectible into our wantlist

    Args:
        collector_id (int): id of the collector that wants to insert to wantlist
        collectible_name (string): name of the collectible to add to wantlist
    
    Return:
        a jasonified dictionary that holds the message, collector_id and 
        collectible_id
    
    Example Output:
    {
        "msg": "Collectible has been added to wantlist successfully!",
        "collector_id": 1,
        "collectible_id": 1,
        "date_added": ???
    }
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the wantlist and collectibles table into our metadata
    wantlist = db.Table("wantlist", metadata, autoload_with=engine)

    # Find the id associated with the collectible_name
    collectible_id = db_collectibles.find_collectible_id(collectible_name)

    curr_date = date.today()

    # Insert a new entry into wantlist table
    insert_stmt = db.insert(wantlist).values(
        {
            "collector_id": collector_id,
            "collectible_id": collectible_id,
            "date_added": curr_date
        }
    )
    conn.execute(insert_stmt)
    conn.close()

    return jsonify(
        {
            "msg": "Collectible has been added to wantlist successfully!",
            "collector_id": collector_id,
            "collectible_id": collectible_id,
            "date_added": curr_date
         }
    ), OK

# TODO: error checking (valid user, valid collectible name)
def remove_from_wantlist(collector_id, collectible_name):
    """Removes a collectible from the user's wantlist, given its name

    Args:
        collector_id (int): id of the collector whose wantlist we want to 
                            remove the collectible from
        collectible_name (string): name of collectible we want to remove from
                                   wantlist
    Returns:
        tuple that contains msg, collector_id and collectible_id
    
    Example Output:
    {
        "msg": "Collectible has been removed from wantlist!",
        "collector_id": 1,
        "collectible_id": 1
    }
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the wantlist table
    want = db.Table("wantlist", metadata, autoload_with=engine)

    # Find the id of the collectible
    collectible_id = db_collectibles.find_collectible_id(collectible_name)

    delete_stmt = db.delete(want).where(
        (want.c.collector_id == collector_id) &
        (want.c.collectible_id == collectible_id))
    
    conn.execute(delete_stmt)
    conn.close()

    return {
        "msg": "Collectible has been removed from wantlist!",
        "collector_id": collector_id,
        "collectible_id": collectible_id
    }