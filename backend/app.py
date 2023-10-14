import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from jinja2.runtime import identity
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import db_manager as dbm
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies, create_refresh_token, set_refresh_cookies
import auth
from datetime import datetime
from datetime import timedelta
from datetime import timezone

def defaultHandler(err):
    response = err.get_response()
    response.data = json.dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

# JWT App Settings
JWTManager(APP)
APP.config["JWT_COOKIE_SECURE"] = False
APP.config["JWT_TOKEN_LOCATION"] = ["cookies"]
APP.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
APP.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
APP.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
APP.config["JWT_COOKIE_CSRF_PROTECT"] = False

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

password = os.environ['POSTGRES_PASSWORD']

APP.register_error_handler(Exception, defaultHandler)


@APP.after_request
def refresh_expiring_jwts(response):
    '''Refreshes users token if it is going to expire withing a given amount of time'''

    exp_in = 60

    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=exp_in))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


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
    '''
    Check if collector already in database via email.
        raises: InputError('Email address already registered')

    '''

    # Get Data
    data = request.get_json()
    email = str(data["email"])
    password = str(data["password"])
    name = str(data["name"])

    password = auth.hash_password(password)

    dbm.insert_collector(email, name, name, '', password, '')

    response = jsonify({'msg': 'Account successfully registered!.'})
    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

@APP.route('/login', methods=['POST'])
def login():
    '''
    check if collector not in database via email
    raise InputError('Email address not registered')
    '''
    # Get Data
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Validate email and passward
    # if not auth.validate_email(email):
    #     raise ValueError("Invalid login email")
    # elif not auth.validate_password(email, password):
    #     raise ValueError("Incorrect Password")

    if not auth.validate_email(email) or not auth.validate_password(email, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Successful login returns acces and refresh tokens to client cookies
    response = jsonify({"msg": "login successful"})
    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

@APP.route('/logout', methods=['POST'])
def logout():
    ''' Removes cookies from client '''

    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@APP.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    '''
    Example of protected route. Requires JWT to access.
    Useful for when user has been logged in for a while and wants to edit profile.
    '''

    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@APP.route("/protected_fresh", methods=["GET"])
@jwt_required(fresh=True)
def protected_fresh():
    '''
    Example of protected route. Requires fresh JWT to be fresh to access.
    Useful for when user has been logged in for a while and wants to edit profile.
    '''

    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@APP.route('/refresh', methods=['POST'])
@jwt_required(fresh=True)
def refresh_token():
    '''
    Refresh access token, makes user have to authenticate credentials again
    '''

    # Create the new access token
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)

    # Retruns a non fresh access token
    response = jsonify({'refresh': True})
    set_access_cookies(response, access_token)
    return response, 200

# for testing api calls
@APP.route('/api')
def api():
    return jsonify({'message': 'This is a unique API call.'})

if __name__ == "__main__":
    APP.run(host ='0.0.0.0')
