import json
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import db_manager as dbm

app = Flask(__name__)
CORS(app)
password = os.environ['POSTGRES_PASSWORD']

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/widgets')
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

@app.route('/initdb')
def db_init():
    dbm.database_setup()

    return 'Database has been setup successfully!'

@app.route('/insertcollector')
def db_collector_insert():
    dbm.insert_collector("bob@gmail.com", "bob222", "bob jacobs","0444444444", "password", "home!")

    return 'Insert has been successful!'

@app.route('/register', methods=['POST'])
def register():
    # check if collector already in database via email
    # raise InputError('Email address already registered')
    dbm.insert_collector(email, name, name, '', password, '')
    return jsonify({'response': 'Account successfully registered!.'})
    # return email + name + password
    # token creation

@app.route('/login', methods=['POST'])
def login():
    # check if collector not in database via email
    # raise InputError('Email address not registered')

    return jsonify({'response': 'Logging in account!.'})


# for testing api calls
@app.route('/api')
def api():
    return jsonify({'message': 'This is a unique API call.'})

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
