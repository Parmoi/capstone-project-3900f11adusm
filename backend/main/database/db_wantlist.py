import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import db_collectibles

""" |------------------------------------|
    |      Functions for wantlist        |
    |------------------------------------| """


# Function to add collectible to wantlist
# TODO: Not done
def insert_wantlist(collector_id, collectible_name):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the wantlist table into our metadata
    wantlist = db.Table("wantlist", metadata, autoload_with=engine)



    # want_insert_stmt = db.insert(wantlist).values(
    #     {
    #         "collector_id": collector_id,
    #         # "collectible_id": db_collectibles.find_collectible_id(collectible_name),
    #     }
    # )
    # conn.execute(want_insert_stmt)

    # conn.close()


    """
    Let's think about this, how do we insert a collectible into a wantlist?

    - If we are give the collectible_name, how do we find its id?
    - collectibles are not stored in the collectible table, but rather individual campaign collectible tables
    - (POSSIBLE SOL) -> add all collectibles to the "collectible" table, that stores coll_id, camp_id, and coll_name
      - collectible_name used to find coll_id and camp_id
      - Join "collectible" table with campaigns to get campaign details (probably only need the name)
      - Join the above joined table with the campaign collectible tables so that we can actually find the collectibles
      - 

    - Information we want in the wantlist: coll_name, coll_


    TODO:
    - when a collectible is added to a campaign, also add the information to the belongs_to table
    
    """


# TODO: Neets to be implemented
def get_wantlist(user_id):
    return {"wantlist": "db_manager.py: get_wantlist() not yet implemented!"}
