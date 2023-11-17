from flask import jsonify
import sqlalchemy as db

import auth
from main.database import db_helpers
from main.error import OK, InputError
from main.privelage import BANNED, COLLECTOR, MANAGER
import main.database.db_manager as dbm

""" |------------------------------------|
    |     Functions for collectors       |
    |------------------------------------| """


def insert_collector(email, username, password, privelage=COLLECTOR):
    """Inserts a collector into the system.

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
    privelages = db.Table("privelages", metadata, autoload_with=engine)

    # Inserts a collector into the collector table
    insert_stmt = db.insert(collectors).values(
        {"email": email, "username": username, "password": password}
    )
    conn.execute(insert_stmt)

    select_stmt = db.select(collectors.c.id).where(collectors.c.email == email)
    cursor = conn.execute(select_stmt)
    collector_id = cursor.fetchone()._asdict().get("id")

    insert_stmt = db.insert(privelages).values(
        {"collector_id": collector_id, "privelage": privelage}
    )
    cursor = conn.execute(insert_stmt)

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
    profile_picture=None,
):
    """Updates the details of a user.

    Args:
        id (int): collector's user id
        email (string): collector's new email
        username (string): collector's new username
        first_name (string): collector's new first name
        last_name (string): collector's new last name
        phone (string): collector's new phone number
        password (string): collector's new hashed password
        address (string): collector's new address

    Returns:
        JSON:
            - on success: {"msg": (string), "collectors": (dictionary)}
        int: success/error code
    """

    update_dict = {k: v for k, v in locals().items() if v != "" and v is not None}
    print(update_dict)

    if "password" in update_dict.keys():
        update_dict["password"] = auth.hash_password(update_dict["password"])

    engine, conn, metadata = dbm.db_connect()

    collectors = db.Table("collectors", metadata, autoload_with=engine)

    update_stmt = db.update(collectors).where(collectors.c.id == id).values(update_dict)
    conn.execute(update_stmt)

    select_stmt = db.select(collectors).where(collectors.c.id == id)
    result = conn.execute(select_stmt)
    collector_info = result.fetchone()._asdict()

    conn.close()

    return (
        jsonify(
            {"msg": "Collector successfully updated!", "collector": collector_info}
        ),
        OK,
    )


def get_all_collectors():
    """get_all_collectors.

    Returns dictionary with collectors value a list of all collectors.
    """
    engine, conn, metadata = dbm.db_connect()
    collectors = db.Table("collectors", metadata, autoload_with=engine)
    privelages = db.Table("privelages", metadata, autoload_with=engine)

    join = db.join(collectors, privelages,
        (collectors.c.id == privelages.c.collector_id))

    select_stmt = db.select(collectors).where(privelages.c.privelage == COLLECTOR).select_from(join)
    result = conn.execute(select_stmt)
    conn.close()

    all_collectors_rows = result.all()
    all_collectors = [row._asdict() for row in all_collectors_rows]

    return jsonify({"collectors": all_collectors}), OK


def get_collector(user_id=None, email=None, username=None):
    """Returns a dict of the collector's details

    Args:
        user_id (int): id of collector we want to find information on
        email (string): string of the collector to find
        username (string): username of the collector to find

    Returns:
        JSON:
            - on success: 
                {
                    "id": (int), 
                    "email": (string), 
                    "username": (string),
                    "first_name": (string),
                    "last_name": (string),
                    "phone": (string),
                    "address": (string),
                    "profile_picture": (string),
                    "twitter_handle": (string),
                    "facebook_handle": (string),
                    "instagram_handle": (string)
                }
            - on error: {"msg": (string)}
        int: success/error code
    
        Raises:
            InputError: Not a valid collector
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table("collectors", metadata, autoload_with=engine)
    select_stmt = None
    if email:
        select_stmt = db.select(collectors).where(collectors.c.email == email)
    elif username:
        select_stmt = db.select(collectors).where(collectors.c.username == username)
    elif user_id:
        select_stmt = db.select(collectors).where(collectors.c.id == user_id)

    result = conn.execute(select_stmt)
    if result is None:
        return jsonify({"msg": "Invalid collector id"}), InputError

    collector_info = result.fetchone()._asdict()
    conn.close()

    return jsonify(collector_info), OK


def get_managers():
    """Return a list of all managers within the system.

    Returns:
        [dictionary]: list of dictionaries of our managers

    stub_return = {
        "managers": [
            {
                "user_id": "3",
                "username": "dso",
                "profile_img": "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api",
                "first_name": "Dyllanson",
                "last_name": "So",
                "email": "ds@gmail.com",
                "phone": "4444 4444",
                "canPublish": True,  # The managers posting privilege
            },
            {
                "user_id": "2",
                "username": "szhang",
                "profile_img": "",
                "first_name": "Stella",
                "last_name": "Zhang",
                "email": "dz@gmail.com",
                "phone": "9999 4444",
                "canPublish": False,  # The managers posting privilege
            },
        ]
    }
    """
    engine, conn, metadata = dbm.db_connect()

    collectors = db.Table("collectors", metadata, autoload_with=engine)
    privelages = db.Table("privelages", metadata, autoload_with=engine)

    join = db.join(
        collectors,
        privelages,
        (privelages.c.privelage == MANAGER)
        & (collectors.c.id == privelages.c.collector_id),
    )

    select_stmt = db.select(
        collectors.c.id.label("user_id"),
        collectors.c.username.label("username"),
        collectors.c.profile_picture.label("profile_img"),
        collectors.c.first_name.label("first_name"),
        collectors.c.last_name.label("last_name"),
        collectors.c.email.label("email"),
        collectors.c.phone.label("phone"),
        privelages.c.privelage.label("privelage"),
    ).select_from(join)

    result = conn.execute(select_stmt)
    managers = db_helpers.rows_to_list(result.fetchall())

    return jsonify({"managers": managers}), OK


def update_socials(user_id, twitter_handle=None, facebook_handle=None, instagram_handle=None):
    """Function to update a user's socials
    
    Args:
        user_id (int): id of the user we want to change the socials for
        twitter (string): twitter handle of user
        facebook (string): facebook handle of the user
        instagram (string): instagram handle of the user

    Returns:
        JSON, int: JSON of success/error message, int of success/error code

    Example Output:
        {"msg": "User 1's socials have been updated}, 200
    """
    engine, conn, metadata = dbm.db_connect()

    # Loads in the collectors table
    ctr = db.Table("collectors", metadata, autoload_with=engine)

    update_dict = {}

    if twitter_handle is not None:
        update_dict["twitter_handle"] = twitter_handle
    if facebook_handle is not None:
        update_dict["facebook_handle"] = facebook_handle
    if instagram_handle is not None:
        update_dict["instagram_handle"] = instagram_handle
    update_stmt = db.update(ctr).where(ctr.c.id == user_id).values(update_dict)
    
    conn.execute(update_stmt)
    conn.close()

    return jsonify({"msg": f"User {user_id}'s socials have been updated!"}), OK


def ban_collector(admin_id, collector_id):
    """Function to ban a certain collector.

    Args:
        admin_id (int): id of admin that is performing the ban
        collector_id (int): id of collector to be banned
    
    """
    engine, conn, metadata = dbm.db_connect()

    privelages = db.Table("privelages", metadata, autoload_with=engine)

    update_stmt = (
        db.update(privelages)
        .where(privelages.c.collector_id == collector_id)
        .values({"privelage": BANNED})
    )
    conn.execute(update_stmt)
    conn.close()

    return


""" |------------------------------------|
    |  Helper functions for collectors   |
    |------------------------------------| """


def get_collector_id(email=None, username=None):
    """Returns the user id associated with an email or username.

    Returns None if user does not exist.

    Args:
        email (string): email of the collector we want to find the id for
        username (string): username of collecter we want to find the id for
    
    Returns:
        int: id of the user
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

    result = conn.execute(select_stmt)

    collector = result.fetchone()
    if collector is None:
        return None

    collector_id = collector._asdict().get("id", None)
    conn.close()
    return collector_id


def get_collector_pw(id=None, email=None):
    """returns the hashed password of a collector through their id or email.

    Args:
        id (int): id of our user
        email (string): email of our user
    
    Returns:
        string: string of the hashed password
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


def get_collector_dict(user_id=None, email=None, username=None):
    """Returns dict with collector's details.

    Args:
        user_id (int): id of the collector we want to find details for

    Returns:
        dictionary: contains the collector's details
    """

    engine, conn, metadata = dbm.db_connect()

    # Loads in the collector table into our metadata
    collectors = db.Table("collectors", metadata, autoload_with=engine)
    select_stmt = None
    if email:
        select_stmt = db.select(collectors).where(collectors.c.email == email)
    elif username:
        select_stmt = db.select(collectors).where(collectors.c.username == username)
    elif user_id:
        select_stmt = db.select(collectors).where(collectors.c.id == user_id)

    result = conn.execute(select_stmt)
    collector_info = result.fetchone()._asdict()
    conn.close()
    return collector_info
