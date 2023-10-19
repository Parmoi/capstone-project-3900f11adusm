import db_manager as dbm
import helpers.hashing as hash
import bcrypt

from flask import jsonify
from flask_jwt_extended import (create_access_token, set_access_cookies, unset_jwt_cookies, 
                                create_refresh_token, set_refresh_cookies)

from error import ( InputError, AccessError, OK )

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
        collector_id = dbm.get_collector_id(email=email)
        if collector_id is None:
            return jsonify({"msg": "Invalid email!"}), InputError
    elif username:
        collector_id = dbm.get_collector_id(username=username)
        if collector_id is None:
            return jsonify({"msg": "Invalid username!"}), InputError
    else:
        return jsonify({"msg": "No email or username provided!"}), InputError

    if not validate_password(email, password):
        return jsonify({"msg": "Invalid password!"}), InputError

    user_id = dbm.get_collector_id(email=email, username=username)
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity=user_id, fresh=True)
    refresh_token = create_refresh_token(identity=user_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK

def logout():
    ''' Removes cookies from client '''
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, OK


def register_collector(email, username, password, first_name = '', last_name='', phone='', address=''):
    """register_collector.

    Checks if email or usernames exists, returns <error_code> if they do.
    Hashes password and inserts the collector into the database.
    Generates access and response tokens and attatches them to response object cookies.
    Returns response for successful collectro registration.

    Args:
        email:
        username:
        name:
        password:
        phone:
        address:
    """
    if email:
        collector_id = dbm.get_collector_id(email=email)
        if collector_id is not None:
            return jsonify({'msg': 'Email address already registered!'}), InputError
    elif username:
        collector_id = dbm.get_collector_id(username=username)
        if collector_id is not None:
            return jsonify({'msg': 'User name already registered!'}), InputError

    password = hash.hash_password(password)

    # TODO: Kinda sloppy handing all theses variables over, wouldn't it be easier to create a class
    collector_id = dbm.insert_collector(email, username, password, first_name = first_name, last_name=last_name, phone=phone, address=address)
    if collector_id is None:
        return jsonify({'msg': 'Account unsuccessfully registered!'}), InputError

    response = jsonify({'msg': 'Account successfully registered!.'})
    access_token = create_access_token(identity=collector_id, fresh=True)
    refresh_token = create_refresh_token(identity=collector_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK


def validate_password(email, password):
    """validate_password.

    Validates users password associated with given email.
    Returns True if password is valid.

    Args:
        email: user email
        password: user password to be validated
    """

    user_hashed_pw_bytes = dbm.get_collector_pw(email=email).encode('utf-8')
    input_pw_bytes = password.encode('utf-8')
    return bcrypt.checkpw(input_pw_bytes, user_hashed_pw_bytes)

def refresh(user_id):
    # TODO: Write docstring clearly explainig what refresh does.
    """refresh.

    Args:
        user_id:
    """
    access_token = create_access_token(identity=user_id)
    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response, OK
