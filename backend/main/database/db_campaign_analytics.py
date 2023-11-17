from flask import jsonify
import sqlalchemy as db

from db_helpers import rows_to_list
from error import OK, InputError, AccessError
import db_manager as dbm

def return_analytics(manager_id):
    """Given a manager, return the analytics for all their campaigns

    Args:
        manager_id (int): id of manager we want to find the analytics for

    Returns:
        JSON: information of our analytics
        int: success/error code

    Example Output:
        {
            [
                {
                    "campaign_id": 5,
                    "campaign_name": "Galapagos Dove",
                    "exchange_dates": ["16/11/2023"],
                    "exchanges_made": [2]
                },
                {
                    "campaign_id": 4,
                    "campaign_name": "Egyptian Viper",
                    "exchange_dates": ["16/11/2023"],
                    "exchanges_made": [1]
                }
            ]
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the campaigns, collectors and exchange_history tables
    camp = db.Table("campaigns", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    eh = db.Table("exchange_history", metadata, autoload_with=engine)

    # Find exchanges where collectible is being sent
    join = db.join(camp, cbl,
        (camp.c.manager_id == manager_id) &
        (cbl.c.campaign_id == camp.c.id)).join(eh,
        (eh.c.collectible_send_id == cbl.c.id) &
        (eh.c.date_accepted >= camp.c.start_date) &
        (eh.c.date_accepted < camp.c.end_date))
    
    outgoing_select_stmt = (db.select(
        camp.c.id.label("campaign_id"),
        camp.c.name.label("campaign_name"),
        eh.c.date_accepted.label("exchange_dates"),
        db.func.count(cbl.c.id).label("exchanges_made"),
    ).group_by(
        camp.c.id, camp.c.name, camp.c.start_date, camp.c.end_date, 
        eh.c.date_accepted
    ).order_by(
        camp.c.id, eh.c.date_accepted
    ).select_from(join))

    outgoing_analytics = rows_to_list(conn.execute(outgoing_select_stmt).fetchall())

    # Find exchanges where collectible is being received
    join = db.join(camp, cbl,
        (camp.c.manager_id == manager_id) &
        (cbl.c.campaign_id == camp.c.id)).join(eh,
        (eh.c.collectible_receive_id == cbl.c.id) &
        (eh.c.date_accepted >= camp.c.start_date) &
        (eh.c.date_accepted < camp.c.end_date))
    
    incoming_select_stmt = (db.select(
        camp.c.id.label("campaign_id"),
        camp.c.name.label("campaign_name"),
        eh.c.date_accepted.label("exchange_dates"),
        db.func.count(cbl.c.id).label("exchanges_made"),
    ).group_by(
        camp.c.id, camp.c.name, camp.c.start_date, camp.c.end_date, 
        eh.c.date_accepted
    ).order_by(
        camp.c.id, eh.c.date_accepted
    ).select_from(join))

    incoming_analytics = rows_to_list(conn.execute(incoming_select_stmt).fetchall())

    all_analytics = outgoing_analytics + incoming_analytics

    result = {}

    for item in all_analytics:
        key = item['campaign_id']
        if key in result:
            result[key]['exchange_dates'].append(item['exchange_dates'])
            result[key]['exchanges_made'].append(item['exchanges_made'])
        else:
            result[key] = {
                'campaign_id': key,
                'campaign_name': item['campaign_name'],
                'exchange_dates': [item['exchange_dates']],
                'exchanges_made': [item['exchanges_made']]
            }

    return jsonify(list(result.values())), OK

