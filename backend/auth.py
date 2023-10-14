import db_manager
import sqlalchemy as db
import bcrypt

# Authentication Protocol
# 1a. New user creates an account, password is hashed and saved in db
# 1b. User logs in, username and password sent to server from react form
# 2. Server creates access_token and refresh_token with secret key
# 3. Server retruns tokens to client stores in cookies
# 4. Every request user makes to protected routes is sent with cookies in the header
#    Some routes may require a fresh token where the user is required to login again
# 5. Server validates tokens
# 6. Server returns response


def validate_email(email):
    engine, conn, metadata = db_manager.db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors).where((collectors.c.email == email))
    execute = conn.execute(select_stmt)
    collector_info = execute.fetchone()._asdict()
    conn.close()
    return collector_info is not None

def hash_password(password):
    pw_bytes = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed_pw.decode('utf-8')


def validate_password(email, password):

    engine, conn, metadata = db_manager.db_connect()
    collectors = db.Table('collectors', metadata, autoload_with=engine)
    select_stmt = db.select(collectors).where((collectors.c.email == email))
    execute = conn.execute(select_stmt)
    user = execute.fetchone()._asdict()
    conn.close()

    user_hashed_pw = user['password'].encode('utf-8')
    input_pw_bytes = password.encode('utf-8')
    return bcrypt.checkpw(input_pw_bytes, user_hashed_pw)

def update_password(password):
    engine, conn, metadata = db_manager.db_connect()
    hashed_pw = hash_password(password)
    return 
