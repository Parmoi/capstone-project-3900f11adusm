import sqlalchemy as db
import psycopg2

# Notes:
# - Database is called "collectible_exchange_db"
# - If table already exists, running the table code won't change it. We have to 
#   delete it first
# - Currently we don't have password hashing just yet
# - Tokens have not been implemented yet either

db_name = "collectible_exchange_db"

# Function to setup our db for the first time
def database_setup():

    # Establish connection
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="password",
        host="localhost"
    )

    conn.autocommit = True

    # Use cursor to create our database if it doesn't exist
    cursor = conn.cursor()
    stmt = f"SELECT * FROM pg_database WHERE datname = '{db_name}'"
    cursor.execute(stmt)
    result = cursor.fetchall()
    if (len(result) == 0):
        create_stmt = f"CREATE DATABASE {db_name}"
        cursor.execute(create_stmt)
    conn.close()

    # Connect to newly made database again
    engine = db.create_engine(f"postgresql://postgres:password@localhost/{db_name}")
    conn = engine.connect()
    metadata = db.MetaData()

    # Creates a collector table and adds it to metadata
    collector_table = db.Table(
        "collectors", metadata, # Names cannot be uppercase
        db.Column("collectorID", db.Integer, db.Identity(),primary_key = True),
        db.Column("email", db.String),
        db.Column("first_name", db.String),
        db.Column("last_name", db.String),
        db.Column("password", db.String)
        # db.Column( "fffff",db.VARBINARY) # For image
    )

    # Creates all tables stored within metadata
    metadata.create_all(engine)

# Function to insert collector into our db
def insert_collector(email, first_name, last_name, password):

    # Create an engine and connect to the db
    engine = db.create_engine(
        f"postgresql://postgres:password@localhost/{db_name}").execution_options(
            isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    metadata = db.MetaData()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values(
        {"email": email, 
         "first_name": first_name, 
         "last_name": last_name, 
         "password": password}
        )
    conn.execute(insert_stmt)

# Code for testing purposes
# database_setup()
# insert_collector("hello@gmail.com", "peter", "bobby", "password")