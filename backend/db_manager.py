import sqlalchemy as db
import psycopg2
import os

db_name = "collectibles_db"
db_user = "postgres"
db_password = os.environ['POSTGRES_PASSWORD']
db_host = "db"

# Function to setup our database
def database_setup():

    # Establish connection
    conn = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host
    )
    conn.autocommit = True

    # Use cursor to create our database if it doesn't exist
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name} WITH (FORCE)")
    cursor.execute(f"CREATE DATABASE {db_name}")
    conn.close()

    # Connect to database again
    engine = db.create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
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
    conn.close()

# Function to insert collector into our db
def insert_collector(email, first_name, last_name, password):

    # Create an engine and connect to the db
    engine = db.create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}").execution_options(
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
    conn.close()