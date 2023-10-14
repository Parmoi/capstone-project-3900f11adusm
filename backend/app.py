import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from jinja2.runtime import identity
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import db_manager as dbm
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import auth


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

@APP.route('/insertcampaign')
def db_campaign_insert():
    dbm.insert_campaign("random campaign", "this is a description", "24/12/2022", "24/12/2023")

    return 'Campaign insert successful!'

@APP.route('/insertcollectible')
def db_collectible_insert():
    dbm.insert_collectible("random collectible", "random campaign")

    return 'Collectible insert successful!'

@APP.route('/insertwantlist')
def db_wantlist_insert():
    dbm.insert_wantlist(1, "random collectible")

    return 'Added collectible to wantlist'

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


# JWT
@app.route('/logintoken', methods=['POST'])
def create_token():
    '''If users login user name and passord correct, generate and return token to user'''
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if check
    # identity = add_claims_to_access_token(email)
    # identity = jwt.user_lookup_loader({ 'identity': email})
    # access_token = create_access_token(email)
    # access_token = auth.create_token(email, password)
    access_token = token = auth.create_token(email)

    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    '''Example of protected route. Requires JWT authentication to access'''
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    # print(current_user)
    # return jsonify(user=current_user), 200
    return jsonify(msg="hello")

if __name__ == "__main__":
    APP.run(host ='0.0.0.0')
