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
    # noinspection PyTypeChecker
    token = get_authorization_token(request)

    user_id = None

    if token:
        try:
            user_id = tokens.get_user_id(request, token)
        except tokens.DecodeError:
            pass

    setattr(request, 'user_id', user_id)
