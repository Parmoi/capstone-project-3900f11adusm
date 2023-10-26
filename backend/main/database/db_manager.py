import sqlalchemy as db
import psycopg2
import os

db_name = "collectibles_db"
db_user = "postgres"
db_password = os.environ["POSTGRES_PASSWORD"]
db_host = "db"

image_url_placeholder = (
    "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg"
)


# Function to setup our database
def database_setup():
    # Establish connection
    conn = psycopg2.connect(user=db_user, password=db_password, host=db_host)
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
        "collectors",
        metadata,  # Names cannot be uppercase
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("email", db.String, unique=True),
        db.Column("username", db.String, unique=True),
        db.Column("first_name", db.String),
        db.Column("last_name", db.String),
        db.Column("phone", db.VARCHAR(10)),
        db.Column("password", db.String),
        db.Column("address", db.String),
        db.Column("profile_picture", db.String),
    )

    # Creates a collectible campaign table
    campaign_table = db.Table(
        "campaigns",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("name", db.String, unique=True),
        db.Column("image", db.String),
        db.Column("description", db.String),
        db.Column("start_date", db.DATE),
        db.Column("end_date", db.DATE),
        db.Column("collectibles_table", db.String),
    )

    # Creates a collectible table
    collectible_table = db.Table(
        "collectibles",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("name", db.String),
        db.Column("image", db.String),
        db.Column("campaign_id", db.Integer, db.ForeignKey("campaigns.id")),
    )

    # Creates a collections table
    collections_table = db.Table(
        "collections",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("campaign_id", db.Integer, db.ForeignKey("campaigns.id")),
        db.Column("collectible_id", db.Integer) 
        # db.Column("user_image", db.String),
        # db.Column("condition", db.String),
    )

    # Creates a wantlist table
    # Ties a user and collectible together
    wantlist_table = db.Table(
        "wantlist",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("date_added", db.DATE)
    )

    # Creates all tables stored within metadata
    metadata.create_all(engine)
    conn.close()


def db_connect():
    """db_connect.

    Function to connect to the db and return [engine, conn, metadata]
    """
    # Create an engine and connect to the db
    engine = db.create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    ).execution_options(isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    metadata = db.MetaData()

    return engine, conn, metadata
