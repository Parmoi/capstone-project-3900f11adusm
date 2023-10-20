import sqlalchemy as db
import db_manager as dbm
from datetime import date

""" |------------------------------------|
    |Functions for collectible_campaigns |
    |------------------------------------| """

# Function to insert new campaign
# * start_date/end_date are string in format "YYYY-MM-DD"
def insert_campaign(name, description, start_date, end_date):

    start_date_obj = date.fromisoformat(start_date)
    end_date_obj = date.fromisoformat(end_date)

    engine, conn, metadata = dbm.db_connect()

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

# Function to convert campaign name to campaign id
# Returns campaign id as int
def find_campaign_id(campaign_name):

    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table('collectible_campaigns', metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.id).where(campaigns.c.name == campaign_name)

    execute = conn.execute(select_stmt)
    campaignId = execute.fetchone()._asdict().get("id")
    conn.close()
    
    return campaignId
