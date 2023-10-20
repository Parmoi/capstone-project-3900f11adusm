import sqlalchemy as db
import db_manager as dbm
import db_collectibles

""" |------------------------------------|
    |      Functions for wantlist        |
    |------------------------------------| """

# Function to add collectible to wantlist
def insert_wantlist(collector_id, collectible_name):
    
    engine, conn, metadata = dbm.db_connect()

    # Loads in the wants table into our metadata
    wantlist = db.Table('wantlist', metadata, autoload_with=engine)

    want_insert_stmt = db.insert(wantlist).values(
        {'collector_id': collector_id,
         'collectible_id': db_collectibles.find_collectible_id(collectible_name)
         })
    conn.execute(want_insert_stmt)

    conn.close()

# TODO: Neets to be implemented
def get_wantlist(user_id):
    return {'wantlist': 'db_manager.py: get_wantlist() not yet implemented!'}
