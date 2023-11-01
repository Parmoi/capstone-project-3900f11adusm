import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_campaigns
import db_helpers
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |     Functions for collectibles     |
    |------------------------------------| """


# TODO: Error checking
def register_collectible(campaign_id, collectible_name, description, image):
    """register_collectible.

    Register a collectible in a campaign.

    Args:
        campaign_id: id of campaign collectible belongs to
        name: name of collectible
        description: description of collectible
        image: Image URL of collectible
        collectible_fields: dictionary of optional fields
    """

    collectible_dict = {
        "name": collectible_name,
        "description": description,
        "image": image,
        "campaign_id": campaign_id,
    }

    engine, conn, metadata = dbm.db_connect()
    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    insert_stmt = db.insert(collectibles).values(collectible_dict)
    conn.execute(insert_stmt)
    conn.close()

    return (
        jsonify(
            {
                "msg": "Collectible {} succesfully registered!".format(
                    collectible_name
                ),
                "campaign_id": campaign_id,
                "collectible_id": find_collectible_id(collectible_name),
            }
        ),
        OK,
    )


def update_collectible(campaign_id, name, description, image, collectible_fields):
    """register_collectible.

    Register a collectible in a campaign.

    Args:
        campaign_id: id of campaign collectible belongs to
        name: name of collectible
        description: description of collectible
        image: Image URL of collectible
        collectible_fields: dictionary of optional fields
    """

def search_collectibles(collectible_name):
    """Find a list of collectibles that match the collectible_name

    Args:
        collectible_name (string): name of collectible we want to find
    
    Returns:
        JSON, int: JSON holds list of collectibles found, int is the error code
    
    Example Output:
    {
        "collectibles": [
            {
                "campaign_name": "random",
                "collectible_description": "hahahahahah!",
                "collectible_image": "",
                "collectible_name": "new_collectible!",
                "date_released": "30/12/2020"
            }
        ]
    }
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectible and campaign tables into our metadata
    coll = db.Table("collectibles", metadata, autoload_with=engine)
    camp = db.Table("campaigns", metadata, autoload_with=engine)

    join = db.join(coll, camp, (coll.c.campaign_id == camp.c.id) &
                               (coll.c.name.ilike(f"%{collectible_name}%")))

    search_stmt = (
        db.select(
            coll.c.name.label("collectible_name"),
            coll.c.image.label("collectible_image"),
            coll.c.description.label("collectible_description"),
            camp.c.name.label("campaign_name"),
            camp.c.start_date.label("date_released"),
        )
        .select_from(join)
    )

    coll_list = db_helpers.rows_to_list(conn.execute(search_stmt).fetchall())

    return jsonify({"collectibles": coll_list}), OK

""" |------------------------------------|
    |  Helper functions for collectibles |
    |------------------------------------| """

def get_collectible(collectible_id):
    """get_collectible.

    Args:
        collectible_id:
    """
    engine, conn, metadata = dbm.db_connect()

    collectibles = db.Table("collectibles", metadata, autoload_with=engine)
    select_stmt = db.select(collectibles).where(collectibles.c.id == collectible_id)
    result = conn.execute(select_stmt)
    conn.close()

    if result is None:
        return {}

    return result.fetchone()._asdict()

# def get_collectible(campaign_id, collectible_id):
#     """get_collectible.

#     Args:
#         campaign_id:
#         collectible_id:
#     """

#     collectible_table_name = db_campaigns.get_campaign_coll_table(campaign_id)

#     engine, conn, metadata = dbm.db_connect()
#     collectibles = db.Table(collectible_table_name, metadata, autoload_with=engine)
#     select_stmt = db.select(collectibles).where(collectibles.c.id == collectible_id)
#     result = conn.execute(select_stmt)
#     conn.close()

#     if result is None:
#         return {}

#     return result.fetchone()._asdict()





def find_collectible_id(collectible_name):
    """Finds the id of the collectible with name collectible_name

    Args:
        collectible_name (string): name of collectible

    Returns:
        int: the id of the collectible
    """
    
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectibles table
    coll = db.Table("collectibles", metadata, autoload_with=engine)

    # Finds and returns the id associated with the collectible_name
    select_stmt = db.select(coll).where(coll.c.name == collectible_name)
    execute = conn.execute(select_stmt)

    return execute.fetchone()._asdict().get("id")



# Function to convert collectible name to collectible id
# Returns collection id as int
# def find_collectible_id(collectible_name):
#     """find_collectible_id.

#     Function to convert collectible name to collectible id
#     Returns collection id as int

#     Args:
#         campaign_id:
#         collectible_name:
#     """
#     engine, conn, metadata = dbm.db_connect()

#     # Loads in the campaign table into our metadata
#     collectibles = db.Table("collectibles", metadata, autoload_with=engine)

#     select_stmt = db.select(collectibles.c.id).where(
#         collectibles.c.name == collectible_name
#     )

#     result = conn.execute(select_stmt)
#     conn.close()
#     if result is None:
#         return None

#     collectible_id = result.fetchone()._asdict().get("id")

#     return collectible_id
