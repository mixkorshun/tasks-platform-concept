from .models import create_user, make_user, get_user_by_credentials
from .password import encode_password


def login(email, password):
    user = get_user_by_credentials(email, password)

    if not user:
        raise LookupError('User not found')

    return user


def register(email, password, type):
    user = create_user(make_user(
        email=email,
        password=encode_password(password),
        type=type,
        balance=0
    ))
    return user
