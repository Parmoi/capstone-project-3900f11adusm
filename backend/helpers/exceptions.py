import json

def defaultHandler(err):
    response = err.get_response()
    response.data = json.dumps({
        "code": err.code,
        "name": "Server Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response