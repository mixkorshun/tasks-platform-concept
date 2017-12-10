from collections import namedtuple

import jwt

from . import settings

secret_key = 'session:' + settings.SECRET_KEY

Store = namedtuple('Store', ('user_id',))


def to_jwt_token(store):
    return jwt.encode(store._asdict(), secret_key).decode()


def from_jwt_token(jwt_token):
    return Store(**jwt.decode(jwt_token.encode(), secret_key))
