import sqlalchemy as db
import db_manager as dbm
import db_campaigns

""" |------------------------------------|
    |     Functions for collectibles     |
    |------------------------------------| """

# Function to add a collectible to db
# * collectible_name: name of collectible we want to insert
# * campaign_name: campaign the collectible belongs to
def insert_collectible(collectible_name, campaign_name):

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectible and belongs_to table into our metadata
    collectibles = db.Table('collectibles', metadata, autoload_with=engine)

    # Adds collectible to collectibles table
    collectible_insert_stmt = db.insert(collectibles).values(
        {"name": collectible_name,
         "image": dbm.image_url_placeholder,
         "campaign_id": db_campaigns.find_campaign_id(campaign_name)}
    )
    
    conn.execute(collectible_insert_stmt)
    conn.close()

# Function to convert collectible name to collectible id
# Returns collection id as int
def find_collectible_id(collectible_name):

    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    collectibles = db.Table('collectibles', metadata, autoload_with=engine)

    select_stmt = db.select(collectibles.c.id).where(collectibles.c.name == collectible_name)

    execute = conn.execute(select_stmt)
    collectibleId = execute.fetchone()._asdict().get("id")
    conn.close()

    # TODO: Value error if doesn't exist or return error code or something?
    
    return collectibleId

def search_collectibles(collectible_name):
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

    engine, conn, metadata = dbm.db_connect()

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
