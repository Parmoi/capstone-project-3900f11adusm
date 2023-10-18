import db_manager as dbm
import helpers.hashing as hash

from flask import jsonify
from flask_jwt_extended import (create_access_token, set_access_cookies, unset_jwt_cookies, 
                                create_refresh_token, set_refresh_cookies)

def login(email, password):
    if not dbm.validate_email(email) or not dbm.validate_password(email, password):
        return jsonify({"status": 401, "msg": "Invalid username and/or password"}), 401

    # Successful login returns access and refresh tokens to client cookies
    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    response = jsonify({"status": 200, "msg": "login successful", 'auth_token': access_token})
    
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200


def register(email, password, name):
    if dbm.validate_email(email):
        return jsonify({"status": 401, "msg": "Email is already registered"}), 401

    password = hash.hash_password(password)
    dbm.insert_collector(email, name, name, '', password, '')

    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    response = jsonify({'status': 200, 'msg': 'Account successfully registered!.', 'auth_token': access_token})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

def logout():
    ''' Removes cookies from client '''

    response = jsonify({"status": 200, "msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200