from flask import request

from project import app
from . import tokens


def get_authorization_token(req):
    if 'Authorization' not in req.headers:
        return None

    authorization = req.headers['Authorization'].split(' ', 1)

    if authorization[0].lower() != 'token':
        return None

    return authorization[1] if len(authorization) > 1 else None


@app.before_request
def before_request():
    token = get_authorization_token(request)

    store = None

    if token:
        try:
            store = tokens.decode(token)
        except tokens.DecodeError:
            pass

    setattr(request, 'session', store)
