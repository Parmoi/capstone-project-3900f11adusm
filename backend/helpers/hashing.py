import main.db_manager as dbm
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

def hash_password(password):
    pw_bytes = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed_pw.decode('utf-8')


def update_password(password):
    engine, conn, metadata = dbm.db_connect()
    hashed_pw = hash_password(password)
    return 
