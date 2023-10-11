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
    engine, conn, metadata = db_connect()

    # Creates a collector table and adds it to metadata
    collector_table = db.Table(
        "collectors", metadata, # Names cannot be uppercase
        db.Column("id", db.Integer, db.Identity(),primary_key = True),
        db.Column("email", db.String),
        db.Column("username", db.String, unique=True),
        db.Column("real_name", db.String),
        db.Column("phone", db.VARCHAR(10)),
        db.Column("password", db.String),
        db.Column("address", db.String),
        db.Column( "profile_picture",db.VARCHAR(20)) # For image
    )

    # Creates a collectible table
    collectible_table = db.Table(
        "collectibles", metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key = True),
        db.Column("name", db.String),
        # db.Column("image", db.VARCHAR) # For image
    )

    # Creates a collectible campaign table
    campaign_table = db.Table(
        "collectible_campaigns", metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key = True),
        db.Column("name", db.String),
        db.Column("description", db.String),
        db.Column("start_date", db.Date),
        db.Column("end_date", db.Date)
    )

    # Creates a wantlist table
    # Ties a user and collectible together
    wantlist_table = db.Table(
        "wants", metadata,
        db.Column("id",db.Integer, db.Identity(), primary_key = True),
        db.Column("collectorID", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectibleID", db.Integer, db.ForeignKey("collectibles.id"))
    )

    # Creates all tables stored within metadata
    metadata.create_all(engine)
    conn.close()

# Function to insert collector into our db
def insert_collector(email, username, real_name, phone, password, address):

    # Create an engine and connect to the db
    engine, conn, metadata = db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values(
        {"email": email, 
         "username": username,
         "real_name": real_name,
         "phone": phone,
         "password": password,
         "address": address}
        )
    conn.execute(insert_stmt)
    conn.close()


# Function to connect to the db and return (engine, conn, metadata)
def db_connect():
    # Create an engine and connect to the db
    engine = db.create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}").execution_options(
            isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    metadata = db.MetaData()

    return engine, conn, metadata