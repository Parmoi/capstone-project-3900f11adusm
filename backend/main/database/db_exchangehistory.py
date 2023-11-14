import sqlalchemy as db
from flask import jsonify
from error import OK, InputError, AccessError
import db_manager as dbm
import db_collections
from db_helpers import rows_to_list
from datetime import datetime, date

# TODO: Error checking
def add_exhange_history(trade_info, engine, conn, metadata):
    """Add an accepted trade offer to our exchange history table

    Args:
        trade_information (): 
    
    Returns:
        JSON, int: JSON of success/error message, int of success/error code

    Example Output:
        {"msg": "Entry into exchange history added successfully!"}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the exchange_history table
    exchange_history = db.Table("exchange_history", metadata, autoload_with=engine)

    # Convert collection ids to collectible ids
    collectible_s_id = db_collections.get_collectible_id(trade_info.get("collection_s_id"))
    collectible_r_id = db_collections.get_collectible_id(trade_info.get("collection_r_id"))

    # Convert the dates from strings to Date objects
    date_offered_obj = datetime.strptime(trade_info.get("date_offered"), "%d/%m/%Y").date()
    date_accepted_obj = datetime.strptime(trade_info.get("date_updated"), "%d/%m/%Y").date()

    eh_insert_stmt = db.insert(exchange_history).values({
        "trade_sender_id": trade_info.get("sender_id"),
        "collectible_send_id": collectible_s_id,
        "trade_receiver_id": trade_info.get("receiver_id"),
        "collectible_receive_id": collectible_r_id,
        "date_offered": date_offered_obj,
        "date_accepted": date_accepted_obj
    })
    conn.execute(eh_insert_stmt)

    return jsonify({"msg": "Entry into exchange history added successfully!"}), OK

# TODO: Error checking
def find_exchange_history(user_id):
    """Finds all exchange history rows that involve the specified collector

    Args:
        user_id (int): id of the collector that we want to find the exchange 
        history for

    Returns:
        JSON, int: JSON of list of all accepted exchanges of user,
                   int of success/error code
    
    Example Output:
        {
            [
                {
                    "exchange_id": "2",
                    "traded_collectible_id": "1",
                    "traded_collectible_name": "Homer",
                    "traded_collectible_img": "https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg",
                    "accepted_collectible_id": "2",
                    "accepted_collectible_name": "Marge",
                    "accepted_collectible_img": "https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api",
                    "trader_collector_id": "2",
                    "trader_profile_img": "default",
                    "trader_username": "person2",
                    "offer_made_date": "2023/10/25",
                    "accepted_date": "2023/10/29",
                },
                {
                    "exchange_id": "3",
                    "traded_collectible_id": "1",
                    "traded_collectible_name": "Bart",
                    "traded_collectible_img": "https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api",
                    "accepted_collectible_id": "2",
                    "accepted_collectible_name": "Dog",
                    "accepted_collectible_img": "https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api",
                    "trader_collector_id": "2",
                    "trader_profile_img": "default",
                    "trader_username": "person2",
                    "offer_made_date": "2023/10/25",
                    "accepted_date": "2023/10/29",
                },
            ]
        }, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the exchange history table
    eh = db.Table("exchange_history", metadata, autoload_with=engine)
    cbl = db.Table("collectibles", metadata, autoload_with=engine)
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    # First find all accepted trades where the user sent the trade
    join = db.join(eh, cbl,
        (eh.c.collectible_send_id == cbl.c.id)).join(ctr,
        (eh.c.trade_sender_id == ctr.c.id) &
        (ctr.c.id == user_id))

    select_stmt = (db.select(
        eh.c.id.label("exchange_id"),
        cbl.c.id.label("traded_collectible_id"),
        cbl.c.name.label("traded_collectible_name"),
        cbl.c.image.label("traded_collectible_img"),
        eh.c.date_offered.label("offer_made_date"),
        eh.c.date_accepted.label("accepted_date"),
        eh.c.trade_receiver_id.label("trader_collector_id"),
        eh.c.collectible_receive_id.label("collectible_receive_id")
    ).select_from(join))

    outgoing_exchanges = rows_to_list(conn.execute(select_stmt).fetchall())

    for exchange in outgoing_exchanges:
        # Find username and profile_img of trade receiver
        trade_r_id = exchange.get("trader_collector_id")
        receiver_select_stmt = (db.select(
            ctr.c.username.label("trader_username"),
            ctr.c.profile_picture.label("trader_profile_img")
        ).where(ctr.c.id == trade_r_id))
        receiver_info = conn.execute(receiver_select_stmt).fetchone()._asdict()
        exchange.update(receiver_info)

        collectible_r_id = exchange.get("collectible_receive_id")
        collectible_select_stmt = (db.select(
            cbl.c.id.label("accepted_collectible_id"),
            cbl.c.name.label("accepted_collectible_name"),
            cbl.c.image.label("accepted_collectible_img")
        ).where(cbl.c.id == collectible_r_id))
        collectible_info = conn.execute(collectible_select_stmt).fetchone()._asdict()
        exchange.update(collectible_info)

    # Second find all accepted trades where user receives the trade
    join = db.join(eh, cbl,
        (eh.c.collectible_receive_id == cbl.c.id)).join(ctr,
        (eh.c.trade_receiver_id == ctr.c.id) &
        (ctr.c.id == user_id))

    select_stmt = (db.select(
        eh.c.id.label("exchange_id"),
        cbl.c.id.label("traded_collectible_id"),
        cbl.c.name.label("traded_collectible_name"),
        cbl.c.image.label("traded_collectible_img"),
        eh.c.date_offered.label("offer_made_date"),
        eh.c.date_accepted.label("accepted_date"),
        eh.c.trade_sender_id.label("trader_collector_id"),
        eh.c.collectible_send_id.label("collectible_send_id")
    ).select_from(join))

    incoming_exchanges = rows_to_list(conn.execute(select_stmt).fetchall())

    for exchange in incoming_exchanges:
        # Find username and profile_img of trade sender
        trade_s_id = exchange.get("trader_collector_id")
        receiver_select_stmt = (db.select(
            ctr.c.username.label("trader_username"),
            ctr.c.profile_picture.label("trader_profile_img")
        ).where(ctr.c.id == trade_s_id))
        receiver_info = conn.execute(receiver_select_stmt).fetchone()._asdict()
        exchange.update(receiver_info)

        collectible_s_id = exchange.get("collectible_send_id")
        collectible_select_stmt = (db.select(
            cbl.c.id.label("accepted_collectible_id"),
            cbl.c.name.label("accepted_collectible_name"),
            cbl.c.image.label("accepted_collectible_img")
        ).where(cbl.c.id == collectible_s_id))
        collectible_info = conn.execute(collectible_select_stmt).fetchone()._asdict()
        exchange.update(collectible_info)

    all_exchanges = outgoing_exchanges + incoming_exchanges

    return jsonify(all_exchanges), OK

