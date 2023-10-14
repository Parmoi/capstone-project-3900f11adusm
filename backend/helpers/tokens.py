import time
import jwt

KEY = 'TOKENKEY'
def generate_token(id):
    payload = {
        'timestamp': time.time(),
        'id': id
    }
    token = jwt.encode(payload, KEY, algorithm='HS256')
    return token.decode()

def get_user(token):
    return jwt.decode(token, KEY, algorithm='HS256')['id']