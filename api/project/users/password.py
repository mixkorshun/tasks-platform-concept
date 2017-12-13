import hashlib

from project import settings

salt = 'users:%s:' % settings.SECRET_KEY


def encode_password(passw):
    return hashlib.sha1((salt + passw).encode()).hexdigest()


def check_password(passw, passw_hash):
    return encode_password(passw) == passw_hash
