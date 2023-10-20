import sqlalchemy as db
from flask import jsonify
import db_manager as dbm
import auth
from main.error import OK, InputError, AccessError

""" |------------------------------------|
    |     Functions for collectors       |
    |------------------------------------| """


def insert_collector(email, username, password):
    """insert_collector.

    Insert a new collector into the database.
    Returns the new users unique id that was created when inserted.

    Args:
        email: collectors email
        username: collectors user name
        password: collectors hashed password
    """
    # Create an engine and connect to the db
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table("collectors", metadata, autoload_with=engine)

    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values(
        {"email": email, "username": username, "password": password}
    )
    conn.execute(insert_stmt)

    select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    cursor = conn.execute(select_stmt)
    collector_id = cursor.fetchone()._asdict().get("id")

    conn.close()

    return (
        jsonify({"msg": "Collector successfully added!", "user_id": collector_id}),
        OK,
    )


def update_collector(
    id,
    email=None,
    username=None,
    first_name=None,
    last_name=None,
    phone=None,
    password=None,
    address=None,
):
    """update_collector.

    Args:
        id: collectors user id
        email: collectors new email
        username: collectors new user name
        first_name: collectors new first name
        last_name: collectors last name
        phone: collectors phone number
        password: collectors hashed password
        address: collectors address
    """

    update_dict = {k: v for k, v in locals().items() if v is not None}

    if "password" in update_dict.keys():
        update_dict["password"] = auth.hash_password(update_dict["password"])

    engine, conn, metadata = dbm.db_connect()

    collectors = db.Table("collectors", metadata, autoload_with=engine)

    update_stmt = db.update(collectors).where(collectors.c.id == id).values(update_dict)
    conn.execute(update_stmt)

    select_stmt = db.select(collectors).where(collectors.c.id == id)
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()

    conn.close()

    return (
        jsonify({"msg": "Collector successfully updated!", "collector": collector_info}),
        OK,
    )


def get_all_collectors():
    """get_all_collectors.

    Returns dictionary with collectors value a list of all collectors.
    """
    engine, conn, metadata = dbm.db_connect()
    collectors = db.Table("collectors", metadata, autoload_with=engine)
    select_stmt = db.select(collectors)
    result = conn.execute(select_stmt)
    conn.close()

    all_collectors_rows = result.all()
    all_collectors = [row._asdict() for row in all_collectors_rows]

    return jsonify({"collectors": all_collectors}), OK



# TODO: user error check
def get_collector(user_id):
    """get_collector.

    Returns dict with collectors details

    Args:
        user_id: user id of collector being returned
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table("collectors", metadata, autoload_with=engine)
    select_stmt = db.select(collectors).where(collectors.c.id == user_id)
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()
    conn.close()

    return jsonify(collector_info), OK

""" |------------------------------------|
    |  Helper functions for collectors   |
    |------------------------------------| """

def get_collector_id(email=None, username=None):
    """get_collector_id.

    Get collectors user id associated with email address or username from database.
    Returns None if user does not exist.

    Args:
        email: users email
        username: users username
    """
    engine, conn, metadata = dbm.db_connect()
    collectors = db.Table("collectors", metadata, autoload_with=engine)

    select_stmt = None
    if email:
        select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    elif username:
        select_stmt = db.select(collectors.c.id).where(
            collectors.c.username == username
        )

    execute = conn.execute(select_stmt)

    execute_return_object = execute.fetchone()
    if execute_return_object is None:
        return None

    collector_id = execute_return_object._asdict().get("id", None)
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
    collectors = db.Table("collectors", metadata, autoload_with=engine)

    select_stmt = None
    if id:
        select_stmt = db.select(collectors).where((collectors.c.id == id))
    elif email:
        select_stmt = db.select(collectors).where((collectors.c.email == email))
    else:
        return None

    execute = conn.execute(select_stmt)
    password = execute.fetchone()._asdict().get("password")
    conn.close()

    return password
