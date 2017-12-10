import jwt

from project import settings
from .models import Store

secret_key = 'session:' + settings.SECRET_KEY


def encode(store):
    return jwt.encode(store._asdict(), secret_key).decode()


def decode(token):
    return Store(**jwt.decode(token.encode(), secret_key))


DecodeError = jwt.DecodeError
