import sqlalchemy as db

username = "newuser"
password = "pass"
host = "localhost"
database_name = "test_db"

def database_setup():
    
    engine = db.create_engine(f"postgresql://{username}:{password}@{host}/{database_name}")
    conn = engine.connect()
    metadata = db.MetaData()

    # Will create collector table and add to the metadata
    collector_table = db.Table(
        "collector", metadata,
        db.Column("collectorID", db.Integer, db.Identity(),primary_key = True),
        db.Column("name", db.String)
    )
    # Creates all tables stored within the metadata
    metadata.create_all(engine)

# Will insert a new collector into the database
def database_collector_insert(name):

    # Create an engine and connect to the db
    engine = db.create_engine(f"postgresql://{username}:{password}@{host}/{database_name}")
    conn = engine.connect()
    metadata = db.MetaData()

    # Loads in the collector table into our metadata
    collectors = db.Table('collector', metadata, autoload_with=engine)

    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values({"name": name})
    conn.execute(insert_stmt)
    conn.commit()



# database_setup()
database_collector_insert("peter")

# Assumptions:
# - A database with name "test_db" should already exist
# - A user with `username` and password `password` must exist
# - We assume that we are working with the local host (can change)