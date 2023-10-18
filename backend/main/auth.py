import db_manager as dbm
import helpers.hashing as hash
import bcrypt

from flask import jsonify
from flask_jwt_extended import (create_access_token, set_access_cookies, unset_jwt_cookies, 
                                create_refresh_token, set_refresh_cookies)


def login(password, email='', username=''):
    """login.

    Args:
        password:
        email:
        username:
    """

    if email:
        collector_id = dbm.get_collector_id(email=email)
        if collector_id is None:
            return jsonify({"msg": "Invalid email!"}), 401
    elif username:
        collector_id = dbm.get_collector_id(username=username)
        if collector_id is None:
            return jsonify({"msg": "Invalid username!"}), 401

    if not validate_password(email, password):
        return jsonify({"msg": "Invalid password!"}), 401

    user_id = dbm.get_collector_id(email=email, username=username)
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity=user_id, fresh=True)
    refresh_token = create_refresh_token(identity=user_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

def logout():
    ''' Removes cookies from client '''

    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200


def register_collector(email, username, password, name='', phone='', address=''):
    """register_collector.

    Args:
        email:
        username:
        name:
        password:
        phone:
        address:
    """

    collector_id = dbm.get_collector_id(email=email)
    if collector_id is not None:
        return jsonify({'msg': 'Email address already registered!'}), 401

    collector_id = dbm.get_collector_id(username=username)
    if collector_id is not None:
        return jsonify({'msg': 'User name already registered!'}), 401

    password = hash.hash_password(password)

    collector_id = dbm.insert_collector(email, username, name, phone, password, address)
    if collector_id is None:
        return jsonify({'msg': 'Account unsuccessfully registered!'}), 401

    response = jsonify({'msg': 'Account successfully registered!.'})
    access_token = create_access_token(identity=collector_id, fresh=True)
    refresh_token = create_refresh_token(identity=collector_id)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

def refresh(user_id):
    """refresh.

    Args:
        user_id:
    """
    access_token = create_access_token(identity=user_id)
    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response, 200

def validate_password(email, password):
    """validate_password.

    Validates users password associated with given email.

    Args:
        email: user email
        password: user password to be validated
    """

    user_hashed_pw = dbm.get_collector_pw(email=email).encode('utf-8')
    input_pw_bytes = password.encode('utf-8')
    return bcrypt.checkpw(input_pw_bytes, user_hashed_pw)

