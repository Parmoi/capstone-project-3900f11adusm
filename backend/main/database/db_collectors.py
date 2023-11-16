import sqlalchemy as db
from flask import jsonify
import auth
import main.database.db_manager as dbm
from main.database import db_helpers
from main.error import OK, InputError, AccessError
from main.privelage import BANNED, COLLECTOR, MANAGER

""" |------------------------------------|
    |     Functions for collectors       |
    |------------------------------------| """


def insert_collector(email, username, password, privelage=COLLECTOR):
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
    select_stmt = db.select(collectors)
    result = conn.execute(select_stmt)
    conn.close()

    all_collectors_rows = result.all()
    all_collectors = [row._asdict() for row in all_collectors_rows]

    return jsonify({"collectors": all_collectors}), OK


# TODO: user error check
def get_collector(user_id=None, email=None, username=None):
    """get_collector.

    Returns dict with collectors details

    Args:
        user_id: user id of collector being returned
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
    """
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

    return jsonify(managers), OK

# TODO: Error checking
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
    engine, conn, metadata = dbm.db_connect()

    privelages = db.Table("privelages", metadata, autoload_with=engine)

    update_stmt = (
        db.update(privelages)
        .where(privelages.c.collector_id == collector_id)
        .values({"privelage": BANNED})
    )
    conn.execute(update_stmt)


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

    result = conn.execute(select_stmt)

    collector = result.fetchone()
    if collector is None:
        return None

    collector_id = collector._asdict().get("id", None)
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


def get_collector_dict(user_id=None, email=None, username=None):
    """get_collector.

    Returns dict with collectors details

    Args:
        user_id: user id of collector being returned
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
