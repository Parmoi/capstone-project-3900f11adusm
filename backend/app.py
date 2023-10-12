import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import db_manager as dbm


def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)
password = os.environ['POSTGRES_PASSWORD']

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

@APP.route('/')
def hello_world():
    return 'Hello, Collector!'

@APP.route('/widgets')
def get_widgets():
    conn = psycopg2.connect(
        host="db",
        user="postgres",
        password=password,
        database="example"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM widgets")

    row_headers=[x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    conn.close()

    return json.dumps(json_data)

@APP.route('/initdb')
def db_init():
    dbm.database_setup()

    return 'Database has been setup successfully!'

@APP.route('/insertcollector')
def db_collector_insert():
    dbm.insert_collector("bob@gmail.com", "bob222", "bob jacobs","0444444444", "password", "home!")

    return 'Insert has been successful!'

@APP.route('/updatecollector')
def db_collector_update():
    dbm.update_collector(1, "bob2@gmail.com", "bob!!!!!!", "bob", "4444444444", "new", "new home!")

    return 'Update has been successful!'

@APP.route('/returncollector')
def db_collector_return():
    return jsonify(dbm.return_collector(1))


@APP.route('/register', methods=['POST'])
def register():
    # check if collector already in database via email
    # raise InputError('Email address already registered')

    # Get Data
    data = request.get_json()
    email = str(data["email"])
    password = str(data["password"])
    name = str(data["name"])

    dbm.insert_collector(email, name, name, '', password, '')
    return jsonify({'response': 'Account successfully registered!.'})
    # return email + name + password
    # token creation

@APP.route('/login', methods=['POST'])
def login():
    # check if collector not in database via email
    # raise InputError('Email address not registered')

    # Get Data
    data = request.get_json()
    email = str(data["email"])
    password = str(data["password"])

    if dbm.validate_account(email, password):
        return jsonify({'response': 'Logging in account!.'})
    else:
        raise ValueError("Invalid login email")

@APP.route('/logout', methods=['POST'])
def logout():
    # remove token/session

    return jsonify({'response': 'Logging out account!.'})

# for testing api calls
@APP.route('/api')
def api():
    return jsonify({'message': 'This is a unique API call.'})

if __name__ == "__main__":
    APP.run(host ='0.0.0.0')
