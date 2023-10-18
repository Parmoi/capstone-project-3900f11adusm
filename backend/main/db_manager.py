import sqlalchemy as db
from datetime import datetime
import psycopg2
import bcrypt
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
        db.Column("collector_id", db.Integer, db.ForeignKey("collectors.id")),
        db.Column("collectible_id", db.Integer, db.ForeignKey("collectibles.id"))
    )

    # Creates a belongs_to †able that ties collectible and campaigns
    belongs_to_table = db.Table(
        "belongs_to", metadata,
        db.Column("id",db.Integer, db.Identity(), primary_key = True),
        db.Column("campaign_id", db.Integer, db.ForeignKey("collectible_campaigns.id")),
        db.Column("collectible_id", db.Integer, db.ForeignKey("collectibles.id"))
    )

    # Creates all tables stored within metadata
    metadata.create_all(engine)
    conn.close()

""" |------------------------------------|
    |     Functions for collectors       |
    |------------------------------------| """

# Function to insert collector into our db
def insert_collector(email, username, real_name, phone, password, address):
    """insert_collector.

    Insert a new collector into the database.
    Returns the new users unique id that was created when inserted.

    Args:
        email: collectors email
        username: collectors user name
        real_name: collectors real name
        phone: collectors phone number
        password: collectors hashed password
        address: collectors address
    """

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

    select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    execute = conn.execute(select_stmt)
    collector_id = execute.fetchone()._asdict().get("id")

    conn.close()

    return collector_id

def update_collector(id, new_email, new_username, new_name, new_phone, new_password, new_address):
    """update_collector.

    Args:
        id:
        new_email:
        new_username:
        new_name:
        new_phone:
        new_password:
        new_address:
    """
    
    engine, conn, metadata = db_connect()
    
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    update_stmt = (db.update(collectors)
                     .where(collectors.c.id == id)
                     .values({
                         'email': new_email,
                         'username': new_username,
                         'real_name': new_name,
                         'phone': new_phone,
                         'password': new_password,
                         'address': new_address
                     }))
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

def get_collector_id(email='', username=''):
    """get_collector_id.

    Get collectors id associated with email address from database

    Args:
        email: users email
    """
    engine, conn, metadata = db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    select_stmt = None
    if email:
        select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    elif username:
        select_stmt = db.select(collectors.c.id).where(collectors.c.username == username)

    execute = conn.execute(select_stmt)
    collector_id = execute.fetchone()._asdict().get("id")
    conn.close()
    return collector_id

def get_collector_pw(id='', email=''):
    engine, conn, metadata = db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    select_stmt = ''
    if id:
        select_stmt = db.select(collectors).where((collectors.c.id == id))
    elif email:
        select_stmt = db.select(collectors).where((collectors.c.email == email))


    execute = conn.execute(select_stmt)
    password = execute.fetchone()._asdict('password')
    conn.close()

    return password

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
    belongs_to = db.Table('belongs_to', metadata, autoload_with=engine)

    # Adds collectible to collectibles table
    collectible_insert_stmt = db.insert(collectibles).values(
        {"name": collectible_name}
    )
    conn.execute(collectible_insert_stmt)

    # Adds belong_to relationship for the collectible
    belongsto_insert_stmt = db.insert(belongs_to).values({
        'campaign_id': find_campaign_id(campaign_name),
        'collectible_id': find_collectible_id(collectible_name)
        })
    conn.execute(belongsto_insert_stmt)

    conn.close()

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
# * start_date/end_date are string in format "DD/MM/YYYY"
def insert_campaign(name, description, start_date, end_date):

    date_format = '%d/%m/%Y'
    start_date_obj = datetime.strptime(start_date, date_format)
    end_date_obj = datetime.strptime(end_date, date_format)

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
