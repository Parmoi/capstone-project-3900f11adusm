import sqlalchemy as db
import db_manager as dbm
from datetime import date

""" |------------------------------------|
    |Functions for collectible_campaigns |
    |------------------------------------| """


def insert_campaign(name, description, start_date, end_date, collectible_fields):
    """insert_campaign.

    Function to insert new campaign

    Args:
        name: name of collectible campaign
        description: description of collectible campaign
        start_date: start_date of campaign ("YYYY-MM-DD")
        end_date: end date of campaign ("YYYY-MM-DD")
    """

    start_date_obj = date.fromisoformat(start_date)
    end_date_obj = date.fromisoformat(end_date)

    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("collectible_campaigns", metadata, autoload_with=engine)

    collectible_table = name + "_collectibles"
    # Adds campaign to collectible_campaigns table
    campaign_insert_stmt = db.insert(campaigns).values(
        {
            "name": name,
            "collectible_table": collectible_table,
            "description": description,
            "start_date": start_date_obj,
            "end_date": end_date_obj,
        }
    )
    conn.execute(campaign_insert_stmt)

    collectible_table = db.Table(
        collectible_table,
        metadata,
        db.Column("id", db.Integer, db.Identity(), primary_key=True),
        *(db.Column(collectible_col) for collectible_col in collectible_fields)
    )

    metadata.create_all(conn)
    conn.close()

    # Create collectible table for this campaign.

    return find_campaign_id(name)


# Function to convert campaign name to campaign id
# Returns campaign id as int
def find_campaign_id(campaign_name):
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaign table into our metadata
    campaigns = db.Table("collectible_campaigns", metadata, autoload_with=engine)

    select_stmt = db.select(campaigns.c.id).where(campaigns.c.name == campaign_name)

    execute = conn.execute(select_stmt)
    campaignId = execute.fetchone()._asdict().get("id")
    conn.close()

    return campaignId
