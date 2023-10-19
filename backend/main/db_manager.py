import sqlalchemy as db
from datetime import date
import psycopg2
import bcrypt
import os

db_name = "collectibles_db"
db_user = "postgres"
db_password = os.environ['POSTGRES_PASSWORD']
db_host = "db"

image_url_placeholder = "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg"

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
        db.Column( "profile_picture",db.String)
    )

    # Creates a collectible table
    collectible_table = db.Table(
        "collectibles", metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key = True),
        db.Column("name", db.String),
        db.Column("image", db.String),
        db.Column("campaign_id", db.Integer, db.ForeignKey("collectible_campaigns.id"))
    )

    # Creates a collectible campaign table
    campaign_table = db.Table(
        "collectible_campaigns", metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key = True),
        db.Column("name", db.String),
        db.Column("image", db.String),
        db.Column("description", db.String),
        db.Column("start_date", db.Date),
        db.Column("end_date", db.Date)
    )

    # Creates a wantlist table
    # Ties a user and collectible together
    wantlist_table = db.Table(
        "wants", metadata,
        db.Column("id",db.Integer, db.Identity(), primary_key = True),
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_id", db.Integer, db.ForeignKey("collectibles.id"))
    )

    # Creates all tables stored within metadata
    metadata.create_all(engine)
    conn.close()

""" |------------------------------------|
    |     Functions for collectors       |
    |------------------------------------| """

# Function to insert collector into our db
def insert_collector(email, username, password):

    # TODO: makes sure user with email does not already exist. Raise exception

    # Create an engine and connect to the db
    engine, conn, metadata = db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values(
        {"email": email, 
         "username": username,
         "password": password}
        )
    conn.execute(insert_stmt)
    conn.close()

# Function to update user information (have to specify the field to change)
def update_collector(id, field, new_info):

    # TODO: Have the function raise an error if the field is not valid

    # possible_fields = ["email", "username", "real_name", "phone", "password", "address"]

    # if field not in possible_fields:
    #     return

    engine, conn, metadata = db_connect()

    collectors = db.Table('collectors', metadata, autoload_with=engine)

    update_stmt = (db.update(collectors)
                   .where(collectors.c.id == id)
                   .values({field : new_info}))
    
    conn.execute(update_stmt)
    conn.close()

# Function returns user info given a user's id
def return_collector(id):

    engine, conn, metadata = db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    select_stmt = db.select(collectors).where(collectors.c.id == id)
    
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()
    conn.close()

    return collector_info

""" |------------------------------------|
    |     Functions for collectibles     |
    |------------------------------------| """

# Function to add a collectible to db
# * collectible_name: name of collectible we want to insert
# * campaign_name: campaign the collectible belongs to
def insert_collectible(collectible_name, campaign_name):

    engine, conn, metadata = db_connect()

    # Loads in the collectible and belongs_to table into our metadata
    collectibles = db.Table('collectibles', metadata, autoload_with=engine)

    # Adds collectible to collectibles table
    collectible_insert_stmt = db.insert(collectibles).values(
        {"name": collectible_name,
         "image": image_url_placeholder,
         "campaign_id": find_campaign_id(campaign_name)}
    )
    
    conn.execute(collectible_insert_stmt)
    conn.close()


"""
Function to return collectibles whose name matches the collectible_name

Example Output:
[
    {
        "campaign_name": "random campaign",
        "collectible_name": "collectible 1",
        "date_released": "Fri, 01 Jan 2021 00:00:00 GMT"
    },
    {
        "campaign_name": "random campaign",
        "collectible_name": "collectible 2",
        "date_released": "Fri, 01 Jan 2021 00:00:00 GMT"
    }
]

"""
def find_collectible(collectible_name):

    engine, conn, metadata = db_connect()

    # Loads in the collectible and campaign tables into our metadata
    collectibles = db.Table('collectibles', metadata, autoload_with=engine)
    campaigns = db.Table('collectible_campaigns', metadata, autoload_with=engine)
    coll = collectibles.alias('coll')
    camp = campaigns.alias('camp')

    joined_tbl = db.join(coll, camp, coll.c.campaign_id == camp.c.id)

    search_stmt = db.select(
        camp.c.name.label("campaign_name"), coll.c.name.label("collectible_name"), camp.c.start_date.label("date_released")
        ).select_from(joined_tbl).where(coll.c.name == collectible_name)

    execute = conn.execute(search_stmt)
    conn.close()

    result_list = []
    results = execute.fetchall()

    for row in results:
        result_list.append(row._asdict())

    return result_list

""" |------------------------------------|
    |      Functions for wantlist        |
    |------------------------------------| """

# Function to add collectible to wantlist
def insert_wantlist(collector_id, collectible_name):
    
    engine, conn, metadata = db_connect()

    # Loads in the wants table into our metadata
    wants = db.Table('wants', metadata, autoload_with=engine)

    want_insert_stmt = db.insert(wants).values(
        {'collector_id': collector_id,
         'collectible_id': find_collectible_id(collectible_name)
         })
    conn.execute(want_insert_stmt)

    conn.close()

""" |------------------------------------|
    |Functions for collectible_campaigns |
    |------------------------------------| """

# Function to insert new campaign
# * start_date/end_date are string in format "YYYY-MM-DD"
def insert_campaign(name, description, start_date, end_date):

    start_date_obj = date.fromisoformat(start_date)
    end_date_obj = date.fromisoformat(end_date)

    engine, conn, metadata = db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table('collectible_campaigns', metadata, autoload_with=engine)

    # Adds campaign to collectible_campaigns table
    campaign_insert_stmt = db.insert(campaigns).values(
        {'name': name,
         'description': description,
         'start_date': start_date_obj,
         'end_date': end_date_obj}
    )
    conn.execute(campaign_insert_stmt)
    conn.close()

""" |------------------------------------|
    |          Helper Functions          |
    |------------------------------------| """

# Function checks if a collector exists in the DB.
def validate_account(email, password):
    engine, conn, metadata = db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    select_stmt = db.select(collectors).where(
                        (collectors.c.email == email) &
                        (collectors.c.password == password))
    
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()
    conn.close()

    return (collector_info is not None)

# Function to connect to the db and return [engine, conn, metadata]
def db_connect():
    # Create an engine and connect to the db
    engine = db.create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}").execution_options(
            isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    metadata = db.MetaData()

    return engine, conn, metadata

# Function to convert collectible name to collectible id
# Returns collection id as int
def find_collectible_id(collectible_name):

    engine, conn, metadata = db_connect()

    # Loads in the campaign table into our metadata
    collectibles = db.Table('collectibles', metadata, autoload_with=engine)

    select_stmt = db.select(collectibles.c.id).where(collectibles.c.name == collectible_name)

    execute = conn.execute(select_stmt)
    collectibleId = execute.fetchone()._asdict().get("id")
    conn.close()
    
    return collectibleId

# Function to convert campaign name to campaign id
# Returns campaign id as int
def find_campaign_id(campaign_name):

    engine, conn, metadata = db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table('collectible_campaigns', metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.id).where(campaigns.c.name == campaign_name)

    execute = conn.execute(select_stmt)
    campaignId = execute.fetchone()._asdict().get("id")
    conn.close()
    
    return campaignId

def validate_email(email):
    engine, conn, metadata = db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors).where((collectors.c.email == email))
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()
    conn.close()
    return collector_info is not None

def validate_password(email, password):

    engine, conn, metadata = db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors).where((collectors.c.email == email))
    execute = conn.execute(select_stmt)
    user = execute.fetchone()._asdict()
    conn.close()

    user_hashed_pw = user['password'].encode('utf-8')
    input_pw_bytes = password.encode('utf-8')
    return bcrypt.checkpw(input_pw_bytes, user_hashed_pw)