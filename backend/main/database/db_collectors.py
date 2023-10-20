import sqlalchemy as db
import db_manager as dbm

""" |------------------------------------|
    |     Functions for collectors       |
    |------------------------------------| """

# # Function to insert collector into our db
# def insert_collector(email, username, password):
#     # Create an engine and connect to the db
#         engine, conn, metadata = db_connect()

#         # Loads in the collector table into our metadata
#         collectors = db.Table('collectors', metadata, autoload_with=engine)

#         # Inserts a collector into the collector table
#         insert_stmt = db.insert(collectors).values(
#             {"email": email, 
#             "username": username,
#             "password": password}
#             )
#         conn.execute(insert_stmt)
#         conn.close()

# TODO: Add first_name and last_name fields to user db, or keep like this i dunno
def insert_collector(email, username, password, first_name='', last_name='',  phone='', address=''):
    """insert_collector.

    Insert a new collector into the database.
    Returns the new users unique id that was created when inserted.

    Args:
        email: collectors email
        username: collectors user name
        first_name: collectors first name
        last_name: collectors last name
        phone: collectors phone number
        password: collectors hashed password
        address: collectors address
    """

    # Create an engine and connect to the db
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)


    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values(
        {"email": email, 
         "username": username,
         "first_name": first_name,
         "last_name": last_name,
         "phone": phone,
         "password": password,
         "address": address}
        )
    conn.execute(insert_stmt)

    select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    cursor = conn.execute(select_stmt)
    collector_id = cursor.fetchone()._asdict().get("id")

    conn.close()
    return collector_id


def update_collector(id, new_email=None, new_username=None, new_first_name=None, new_last_name=None, new_phone=None, new_password=None, new_address=None):
    """update_collector.

    Args:
        id: collectors user id
        new_email: collectors new email
        new_username: collectors new user name
        new_first_name: collectors new first name
        new_last_name: collectors last name
        new_phone: collectors phone number
        new_password: collectors hashed password
        new_address: collectors address
    """
    
    engine, conn, metadata = dbm.db_connect()

    collectors = db.Table('collectors', metadata, autoload_with=engine)

    update_stmt = (db.update(collectors)
                     .where(collectors.c.id == id)
                     .values({
                         'email': new_email,
                         'username': new_username,
                         "first_name": new_first_name,
                         "last_name": new_last_name,
                         'phone': new_phone,
                         'password': new_password,
                         'address': new_address
                     }))
    conn.execute(update_stmt)

    conn.close()


def get_all_collectors():
    """get_all_collectors.
    
    Returns dictionary of all collectors with collectors user id as key.
    """
    engine, conn, metadata = dbm.db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors)
    result = conn.execute(select_stmt)

    all_collectors_rows = result.all()
    all_collectors = [row._asdict() for row in all_collectors_rows]
    all_collectors_dict = dict()
    for collector in all_collectors:
        all_collectors_dict[collector['id']] = collector

    return all_collectors_dict


# Function returns user info given a user's id
def get_collector(user_id):
    """get_collector.

    Returns dict with collectors details

    Args:
        user_id: user id of collector being returned
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors).where(collectors.c.id == user_id)
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()
    conn.close()

    return collector_info

def get_collector_id(email=None, username=None):
    """get_collector_id.

    Get collectors user id associated with email address or username from database.
    Returns None if user does not exist.

    Args:
        email: users email
        username: users username
    """
    engine, conn, metadata = dbm.db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    select_stmt = None
    if email:
        select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    elif username:
        select_stmt = db.select(collectors.c.id).where(collectors.c.username == username)

    execute = conn.execute(select_stmt)

    execute_return_object = execute.fetchone()
    if execute_return_object is None:
        return None

    collector_id = execute_return_object._asdict().get('id', None)
    conn.close()
    return collector_id


# TODO: do a check that the collector acturally exists
def get_collector_pw(id=None, email=None):
    """get_wantlist.

    Returns the hashed password of the user associated with user_id or email.
    Returns None if id and email not given.

    Args:
        id: users id
        email: users email
    """
    engine, conn, metadata = dbm.db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)

    select_stmt = None
    if id:
        select_stmt = db.select(collectors).where((collectors.c.id == id))
    elif email:
        select_stmt = db.select(collectors).where((collectors.c.email == email))
    else:
        return None

    execute = conn.execute(select_stmt)
    password = execute.fetchone()._asdict().get('password')
    conn.close()

    return password
