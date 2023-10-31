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
        JSON, int: JSON holds the wantlist, int is the error code
    
    Example Output:
    {
        [
            {
                "id": 1, (id of collection)
                "collectible_id": 1,
                "name": "new_collectible!", (name of collectible)
                "image": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                "campaign_id": 1,
                "campaign_name": "random",
                "date_added": "29/10/2023",
                "date_released": "30/12/2020"
            },
            {
                "id": 1, (id of collection)
                "name": "another_collectible!", (id of collection)
                "collectible_id": 2,
                "image": "",
                "campaign_id": 1,
                "campaign_name": "random",
                "date_added": "29/10/2023",
                "date_released": "30/12/2020"
            }
        ]
    }, OK
    """
    engine, conn, metadata = dbm.db_connect()

    # Load in the wantlist, campaign and collectible tables
    want = db.Table("wantlist", metadata, autoload_with=engine)
    coll = db.Table("collectibles", metadata, autoload_with=engine)
    camp = db.Table("campaigns", metadata, autoload_with=engine)

    # Join the tables
    join = db.join(want, coll, 
                   (want.c.collector_id == user_id) & 
                   (want.c.collectible_id == coll.c.id)
                   ).join(camp, coll.c.campaign_id == camp.c.id)
    
    search_stmt = (
        db.select(
            coll.c.id.label("collectible_id"),
            coll.c.name.label("name"),
            coll.c.image.label("image"),
            camp.c.id.label("campaign_id"),
            camp.c.name.label("campaign_name"),
            want.c.date_added.label("date_added"),
            camp.c.start_date.label("date_released")
        )
        .select_from(join)
    )

    wantlist = db_helpers.rows_to_list(conn.execute(search_stmt).fetchall())
    conn.close()

    # Stub of wantlist requires "id" (of collection), but I'm not too sure how
    # it works, so for now we will add "id": 1 to all dictionaries
    for want_dict in wantlist:
        want_dict["id"] = 1

    return jsonify(wantlist), OK


# TODO: Error checking (valid user, valid collectible name)
def insert_wantlist(collector_id, collectible_name):
    """Function to insert a collectible into our wantlist

    Args:
        collector_id (int): id of the collector that wants to insert to wantlist
        collectible_name (string): name of the collectible to add to wantlist
    
    Return:
        JSON, int: JSON that holds the wantlist id, int is the error code
    
    Example Output:
        {"wantlist_id": 1}, 200
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

    wantlist_id = find_wantlist_id(collector_id, collectible_name)

    return jsonify({"wantlist_id": wantlist_id}), OK

# TODO: error checking (valid user, valid collectible name)
def remove_from_wantlist(collector_id, collectible_name):
    """Removes a collectible from the user's wantlist, given its name

    Args:
        collector_id (int): id of the collector whose wantlist we want to 
                            remove the collectible from
        collectible_name (string): name of collectible we want to remove from
                                   wantlist
    Returns:
        JSON, id: JSON of our wantlist id, and id of the error code
    
    Example Output:
        {"wantlist_id": 1}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the wantlist table
    want = db.Table("wantlist", metadata, autoload_with=engine)

    # Find the id of the collectible
    collectible_id = db_collectibles.find_collectible_id(collectible_name)

    # Find the wantlist_id of this interaction
    wantlist_id = find_wantlist_id(collector_id, collectible_name)

    delete_stmt = db.delete(want).where(
        (want.c.collector_id == collector_id) &
        (want.c.collectible_id == collectible_id))
    
    conn.execute(delete_stmt)
    conn.close()

    return jsonify({"wantlist_id": wantlist_id}), OK

def find_wantlist_id(collector_id, collectible_name):
    """Give the wantlist_id that corresponds to the given collector and collectible

    Args:
        collector_id (int): id of the collector
        collectible_name (string): name of the collectible
    
    Returns:
        int: int corresponding to wantlist row that matches collector id and
             collectible name
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in our wantlist table
    want = db.Table("wantlist", metadata, autoload_with=engine)

    # Find the id associated with the collectible_name
    collectible_id = db_collectibles.find_collectible_id(collectible_name)

    select_stmt = db.select(want.c.id).where(
        (want.c.collector_id == collector_id) & 
        (want.c.collectible_id == collectible_id))

    # Find and return the corresponding wantlist id
    wantlist_id = conn.execute(select_stmt).fetchone()._asdict().get("id")
    conn.close()

    return wantlist_id
