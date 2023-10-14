from flask import Flask, jsonify, request
from flask_cors import CORS

import helpers.config as config
import helpers.exceptions as exceptions

from main import db_manager as dbm
from main import auth

APP = Flask(__name__)
APP.config.from_object(config.DevelopmentConfig)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, exceptions.defaultHandler)

CORS(APP)

@APP.route('/initdb')
def db_init():
    dbm.database_setup()
    return 'Database has been setup successfully!'

@APP.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = str(data["email"])
    password = str(data["password"])
    name = str(data["name"])

    return jsonify(auth.register(name, email, password))

@APP.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = str(data["email"])
    password = str(data["password"])

    return jsonify(auth.login(email, password))

@APP.route('/logout', methods=['POST'])
def logout():
    # remove token/session

    return jsonify({'response': 'Logging out account!.'})


if __name__ == "__main__":
    APP.run(host =config.host, port=config.port)
