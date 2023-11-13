import sqlalchemy as db
from flask import jsonify
from error import OK, InputError, AccessError
import db_manager as dbm

# TODO: Error checking
def add_exhange_history(trade_information):
    """Add an accepted trade offer to our exchange history table

    Args:
        trade_information (): 
    
    Returns:
        ...

    Example Output:
        ...
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the exchange_history table
    

    return

# TODO: Error checking
def find_id():
    return