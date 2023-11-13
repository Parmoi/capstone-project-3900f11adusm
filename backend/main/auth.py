import sqlalchemy as db
from database import db_collectors
import bcrypt

from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    create_refresh_token,
    set_refresh_cookies,
)


from privelage import COLLECTOR, MANAGER, ADMIN
from main.database import db_manager as dbm
from main.database import db_collectors
from error import InputError, AccessError, OK

""" |------------------------------------|
    |     Functions for Authorization    |
    |------------------------------------| """


def login(password, email=None, username=None):
    """login.

    Logs a user in by setting fresh access and refresh tokens in client cookies
    if credentials are correct.

    Args:
        password: users password
        email: users email
        username: users username

    provide username or email, not both.
    """
    if email:
        collector_id = db_collectors.get_collector_id(email=email)
        if collector_id is None:
            return jsonify({"msg": "Invalid email!"}), InputError
    elif username:
        collector_id = db_collectors.get_collector_id(username=username)
        if collector_id is None:
            return jsonify({"msg": "Invalid username!"}), InputError
    else:
        return jsonify({"msg": "No email or username provided!"}), InputError

    if not validate_password(email, password):
        return jsonify({"msg": "Invalid password!"}), InputError

    user_id = db_collectors.get_collector_id(email=email, username=username)
    response = jsonify(
        {"userId": user_id, "privelage": get_user_privelage(user_id)}
    )
    access_token = create_access_token(identity=user_id, fresh=True)
    refresh_token = create_refresh_token(identity=user_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK


def logout():
    """Removes cookies from client"""
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, OK


def register_collector(email, username, password, privelage=COLLECTOR):
    """register_collector.

    Checks if email or usernames exists, returns <error_code> if they do.
    Hashes password and inserts the collector into the database.
    Generates access and response tokens and attatches them to response object cookies.
    Returns response for successful collector registration.

    Args:
        email:
        username:
        password:
    """

    collector_id = db_collectors.get_collector_id(email=email, username=username)
    if collector_id is not None:
        return jsonify({"msg": "Email or user name already registered!"}), InputError

    password = hash_password(password)

    resp, status = db_collectors.insert_collector(
        email,
        username,
        password,
        privelage
    )

    if status != OK:
        return jsonify({"msg": "Account unsuccessfully registered!"}), status

    collector_id = db_collectors.get_collector_id(email=email, username=username)

    response = jsonify({"msg": "Account successfully registered!"})
    access_token = create_access_token(identity=collector_id, fresh=True)
    refresh_token = create_refresh_token(identity=collector_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK


def refresh(user_id):
    # TODO: Write docstring clearly explainig what refresh does.
    """refresh.

    Args:
        user_id:
    """
    access_token = create_access_token(identity=user_id)
    response = jsonify({"refresh": True})
    set_access_cookies(response, access_token)
    return response, OK


def get_privelage(user_id):
    user_privelage = get_user_privelage(user_id)
    return jsonify({"privelage": user_privelage}), OK


def update_privelage(user_id, privelage):
    engine, conn, metadata = dbm.db_connect()

    privelages = db.Table("privelages", metadata, autoload_with=engine)

    update_stmt = (
        db.update(privelages)
        .where(privelages.c.collector_id == user_id)
        .values({"privelage": privelage})
    )
    conn.execute(update_stmt)
    conn.close()

    user_privelage = get_user_privelage(user_id)

    return jsonify({"privelage": user_privelage}), OK


def check_privelage(user_id, required_privelage):
    user_privelage = get_user_privelage(user_id)
    has_privelage = user_privelage >= required_privelage

    if not has_privelage:
        return jsonify(
            {
                "msg": "user {} has privelage level {}, requires at least privelage level {}!".format(
                    user_id, user_privelage, required_privelage
                ),
                "privelage": user_privelage,
            },
            AccessError,
        )
    else:
        return jsonify({"privelage": user_privelage})


""" |------------------------------------|
    | Helper functions for Authorization |
    |------------------------------------| """


# TODO: Return proper error on user does not exist
def validate_password(email, password):
    """validate_password.

    Validates users password associated with given email.
    Returns True if password is valid.

    Args:
        email: user email
        password: user password to be validated
    """

    user_hashed_pw = db_collectors.get_collector_pw(email=email)
    # collector = db_collectors.get_collector(email=email)
    if user_hashed_pw is not None:
        user_hashed_pw_bytes = user_hashed_pw.encode("utf-8")
        input_pw_bytes = password.encode("utf-8")
        return bcrypt.checkpw(input_pw_bytes, user_hashed_pw_bytes)
    else:
        return


def hash_password(password):
    pw_bytes = password.encode("utf-8")
    hashed_pw = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed_pw.decode("utf-8")


def get_user_privelage(user_id):
    engine, conn, metadata = dbm.db_connect()
    privelages = db.Table("privelages", metadata, autoload_with=engine)
    select_stmt = db.select(privelages.c.privelage).where(
        privelages.c.collector_id == user_id
    )
    res = conn.execute(select_stmt)
    conn.close()

    user_privelage = res.fetchone()._asdict().get("privelage")
    return user_privelage


def check_user_privelage(user_id, required_privelage):
    user_privelage = get_user_privelage(user_id)
    return user_privelage >= required_privelage
