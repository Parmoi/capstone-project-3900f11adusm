import app
import db_manager
import sqlalchemy as db
from flask import jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import os
import jwt






# Authentication Protocol
# 1a. New user creates an account, password is hashed and saved in db
# 1b. User logs in, username and password sent to server from react form
# 2. Server creates JWT with secret key
# 3. Server retruns JWT to user and client stores in cookie
# 4. Every request user makes to protected routes is sent with JWT in header
# 5. Server validates JWT
# 6. Server returns response


# Other Considerations:
# Could use Google Oauth2 
# Authentication vs Athorization
# Blacklist for expired/unauthorized tokens (possibly client side to be stored)



def hash_password(password):
    salt = os.environ["AUTH_SALT"]
    hashed_pw = bcrypt.hash_pw(password, salt)
    return hashed_pw

def validate_password(username, password):

    # engine, conn, metadata = db_manager.db_connect()
    # collectors = db.Table('collectors', metadata, autoload_with=engine)
    # select_stmt = db.select(collectors.c.password).where(collectors.c.id == id)
    # execute = conn.execute(select_stmt)
    # user_hashed_pw = execute.fetchone()._asdict()
    # conn.close()

    user = db_manager.return_collector(username)
    user_hashed_pw = user.password
    hashed_pw = hash_password(password)
    return user_hashed_pw == hashed_pw



def create_token(id):
    user = db_manager.return_collector(id)
    encoded_jwt = jwt.encode({
        'iss': 
        })

    access_token = create_access_token(indentity=email)
    return jsonify(access_token)


def validate_token(token):
    validation_status = True
    return validation_status


def update_password(password):
    engine, conn, metadata = db_manager.db_connect()
    hashed_pw = hash_password(password)






    return 


    
    
