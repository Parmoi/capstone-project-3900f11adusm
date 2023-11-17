from datetime import date
from flask import jsonify
import sqlalchemy as db

from error import OK
import db_collections, db_helpers, db_manager as dbm

""" |------------------------------------|
    |      Functions for wantlist        |
    |------------------------------------| """


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
    join = db.join(
        want,
        coll,
        (want.c.collector_id == user_id) & (want.c.collectible_id == coll.c.id),
    ).join(camp, coll.c.campaign_id == camp.c.id)

    search_stmt = db.select(
        want.c.id.label("id"),
        coll.c.id.label("collectible_id"),
        coll.c.name.label("name"),
        coll.c.image.label("image"),
        camp.c.id.label("campaign_id"),
        camp.c.name.label("campaign_name"),
        want.c.date_added.label("date_added"),
        camp.c.start_date.label("date_released"),
    ).select_from(join)

    wantlist = db_helpers.rows_to_list(conn.execute(search_stmt).fetchall())
    conn.close()

    return jsonify(wantlist), OK


def insert_wantlist(collector_id, collectible_id):
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

    curr_date = date.today()

    # Insert a new entry into wantlist table
    insert_stmt = db.insert(wantlist).values(
        {
            "collector_id": collector_id,
            "collectible_id": collectible_id,
            "date_added": curr_date,
        }
    )
    conn.execute(insert_stmt)
    conn.close()

    wantlist_id = find_last_wantlist(collector_id).get("id")

    return jsonify({"wantlist_id": wantlist_id}), OK


def remove_from_wantlist(collector_id, wantlist_id):
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

    want = db.Table("wantlist", metadata, autoload_with=engine)

    delete_stmt = db.delete(want).where(
        (want.c.collector_id == collector_id) & (want.c.id == wantlist_id)
    )

    conn.execute(delete_stmt)
    conn.close()

    return jsonify({"wantlist_id": wantlist_id}), OK


def move_to_collection(collector_id, wantlist_id):
    """Moves wantlist collectible to collectors collection and removes it from wantlist

    Args:
        collector_id (int): id of collector
        wantlist_id (int): id of wantlist row
    """
    collectible_id = get_wantlist_dict(wantlist_id).get("collectible_id")

    db_collections.insert_collectible(collector_id, collectible_id)
    remove_from_wantlist(collector_id, wantlist_id)

    collection = db_collections.get_last_collection(collector_id)

    return jsonify({"collection_id": collection.get("id")})


""" |------------------------------------|
    |    Helper Functions for wantlist   |
    |------------------------------------| """


def find_wantlist_id(collector_id, collectible_id):
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

    select_stmt = db.select(want.c.id).where(
        (want.c.collector_id == collector_id)
        & (want.c.collectible_id == collectible_id)
    )

    # Find and return the corresponding wantlist id
    wantlist_id = conn.execute(select_stmt).fetchone()._asdict().get("id")
    conn.close()

    return wantlist_id


def find_last_wantlist(collector_id):
    """Find the last item in the collector's wantlist.
    
    Args:
        collector_id (int): id we want to find the last wantlist item for
    
    Returns:
        dictionary: dictionary of the last wantlist item of the collector
    """
    engine, conn, metadata = dbm.db_connect()
    wantlist = db.Table("wantlist", metadata, autoload_with=engine)
    select_stmt = (
        db.select(wantlist)
        .where(wantlist.c.collector_id == collector_id)
        .order_by(wantlist.c.id.desc())
    )
    results = conn.execute(select_stmt)
    conn.close()

    wantlist_dict = results.fetchone()._asdict()
    return wantlist_dict


def get_wantlist_dict(wantlist_id):
    """Return a dictionary containing the details of a wantlist.
    
    Args:
        wantlist_id (int): id of wantlist we want the information for

    Returns:
        dictionary: dictionary of the wantlist

    """
    engine, conn, metadata = dbm.db_connect()

    wantlist = db.Table("wantlist", metadata, autoload_with=engine)

    select_stmt = db.select(wantlist).where(wantlist.c.id == wantlist_id)
    res = conn.execute(select_stmt)
    conn.close()

    wantlist_dict = res.fetchone()._asdict()
    return wantlist_dict
