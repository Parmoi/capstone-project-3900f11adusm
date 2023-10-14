import db_manager as dbm
import helpers.hashing as hash

from flask import jsonify
from flask_jwt_extended import (create_access_token, set_access_cookies, unset_jwt_cookies, 
                                create_refresh_token, set_refresh_cookies)

def login(email, password):
    '''
    check if collector not in database via email
    raise InputError('Email address not registered')
    '''
    if not dbm.validate_email(email) or not dbm.validate_password(email, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Successful login returns acces and refresh tokens to client cookies
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200


def register(email, password, name):
    '''
    Check if collector already in database via email.
        raises: InputError('Email address already registered')

    '''

    password = hash.hash_password(password)
    dbm.insert_collector(email, name, name, '', password, '')

    response = jsonify({'msg': 'Account successfully registered!.'})
    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

def logout():
    ''' Removes cookies from client '''

    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200