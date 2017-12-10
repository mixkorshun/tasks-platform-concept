from functools import wraps

from flask import request
from werkzeug.exceptions import Forbidden


def only_authorized(view):
    @wraps
    def inner(*args, **kwargs):
        if not request.session or not request.session.user_id:
            raise Forbidden(
                'Missed or invalid `Authorization` header.'
            )

        return view(*args, **kwargs)

    return inner
