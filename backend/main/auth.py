import db_manager as dbm
import helpers.hashing as hash

from flask import jsonify
from flask_jwt_extended import (create_access_token, set_access_cookies, unset_jwt_cookies, 
                                create_refresh_token, set_refresh_cookies)

from error import ( InputError, AccessError, OK )

def login(email, password):
    if not dbm.validate_email(email) or not dbm.validate_password(email, password):
        return jsonify({"status": InputError, "msg": "Invalid username and/or password"}), InputError

    # Successful login returns access and refresh tokens to client cookies
    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    response = jsonify({"status": OK, "msg": "login successful", 'auth_token': access_token})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK


def register(email, password, name):
    if dbm.validate_email(email):
        return jsonify({"status": InputError, "msg": "Email is already registered"}), InputError

    password = hash.hash_password(password)
    dbm.insert_collector(email, name, name, '', password, '')

    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    response = jsonify({'status': OK, 'msg': 'Account successfully registered!.', 'auth_token': access_token})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, OK

def logout():
    ''' Removes cookies from client '''

    response = jsonify({"status": OK, "msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, OK