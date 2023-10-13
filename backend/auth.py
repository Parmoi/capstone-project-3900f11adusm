import db_manager
import sqlalchemy as db
from flask import jsonify
from flask_jwt_extended import create_access_token
import bcrypt






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
# Blacklist for expired/unauthorized tokens (possibly client side to be stored)



def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hash_pw(password, salt)
    return hashed_pw

def validate_password(password):

    engine, conn, metadata = db_manager.db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors.password).where(collectors.c.id == id)
    execute = conn.execute(select_stmt)
    user_hashed_pw = execute.fetchone()._asdict()

    conn.close()

    hashed_pw = hash_password(password)

    user_hashed_pw = "Get hashed password from database"


    return user_hashed_pw == bcrypt.hash_pw(password, salt)



def create_token(email):
    access_token = create_access_token(indentity=email)
    return jsonify(access_token)


def validate_token(token):
    validation_status = True
    return validation_status


def update_password(password):
    engine, conn, metadata = db_manager.db_connect()
    hashed_pw = hash_password(password)




    return 


