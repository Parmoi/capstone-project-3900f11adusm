import sqlalchemy as db
import psycopg2
import os

db_name = "collectibles_db"
db_user = "postgres"
db_password = os.environ["POSTGRES_PASSWORD"]
db_host = "db"

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

    # Connect to the database
    engine, conn, metadata = db_connect()

    # Table that stores all collectibles
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
        db.Column("twitter_handle", db.String),
        db.Column("facebook_handle", db.String),
        db.Column("instagram_handle", db.String),
    )

    # Table that stores all campaigns
    campaign_table = db.Table(
        "campaigns",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("name", db.String, unique=True),
        db.Column("image", db.String),
        db.Column("description", db.String),
        db.Column("manager_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("start_date", db.DATE),
        db.Column("end_date", db.DATE),
        db.Column("approved", db.Boolean),
    )

    # Table that stores all campaign feedback
    campaign_feedback_table = db.Table(
        "campaign_feedback",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("campaign_id", db.Integer, db.ForeignKey("campaigns.id")),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("feedback", db.String),
        db.Column("feedback_date", db.DATE),
    )

    # Table that stores all collectibles
    collectible_table = db.Table(
        "collectibles",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("name", db.String),
        db.Column("description", db.String),
        db.Column("image", db.String),
        db.Column("campaign_id", db.Integer, db.ForeignKey("campaigns.id")),
    )

    # Table that stores what collectibles belong to what user's collection
    collections_table = db.Table(
        "collections",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("date_added", db.DATE),
    )

    # Table that stores what collectibles a user wants
    wantlist_table = db.Table(
        "wantlist",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("date_added", db.DATE),
    )

    # Table that lists all current trade posts
    trade_posts_table = db.Table(
        "trade_posts",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collection_id", db.Integer, db.ForeignKey("collections.id")),
        db.Column("post_title", db.String),
        db.Column("post_description", db.String),
        db.Column("post_date", db.DATE)
    )

    # Table that stores the images of the trade posts
    trade_post_images_table = db.Table(
        "trade_post_images",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("trade_post_id", db.Integer, db.ForeignKey("trade_posts.id")),
        db.Column("name", db.String),
        db.Column("caption", db.String),
        db.Column("image_url", db.String)
    )

    # Table that stores all sent trade offers
    trade_offers_table = db.Table(
        "trade_offers",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("trade_post_id", db.Integer, db.ForeignKey("trade_posts.id")),
        db.Column("trade_sender_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collection_send_id", db.Integer, db.ForeignKey("collections.id")),
        db.Column("offer_message", db.String),
        db.Column("offer_image", db.String),
        db.Column("offer_status", db.String),
        db.Column("date_offered", db.DATE),
        db.Column("date_updated", db.DATE),
    )

    # Table that stores all accepted/declined offers
    past_trade_offers_table = db.Table(
        "past_trade_offers",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("trade_sender_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_send_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("trade_receiver_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_receive_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("offer_status", db.String),
        db.Column("date_offered", db.DATE),
        db.Column("date_updated", db.DATE),
    )

    # Table that stores all accepted trade interactions
    exchange_history_table = db.Table(
        "exchange_history",
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        db.Column("trade_sender_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_send_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("trade_receiver_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_receive_id", db.Integer, db.ForeignKey("collectibles.id")),
        db.Column("date_offered", db.DATE),
        db.Column("date_accepted", db.DATE),
    )

    # Table that stores the privelages of a certain user
    privelage_table = db.Table(
        "privelages",
        metadata,
        db.Column(
            "collector_id", db.Integer, db.ForeignKey("collectors.id"), primary_key=True
        ),
        db.Column("privelage", db.Integer),
        db.Column("code", db.Integer)
    )

    # Creates all tables stored within metadata
    metadata.create_all(engine)
    conn.close()


def db_connect():
    """Function to connect to the db and return [engine, conn, metadata].
    """
    # Create an engine and connect to the db
    engine = db.create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    ).execution_options(isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    metadata = db.MetaData()

    return engine, conn, metadata
