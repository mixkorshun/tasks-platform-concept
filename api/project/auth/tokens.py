import jwt

from project import settings

secret_key = 'session:' + settings.SECRET_KEY


def get_token(user_id):
    return jwt.encode({'uid': user_id}, secret_key).decode()


def get_user_id(token):
    return jwt.decode(token.encode(), secret_key)['uid']


DecodeError = jwt.DecodeError
