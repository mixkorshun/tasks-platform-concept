from functools import wraps

from flask import request
from werkzeug.exceptions import Forbidden


def only_authorized(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not _is_authorized(request):
            raise Forbidden(
                'Missed or invalid `Authorization` header.'
            )

        return view(*args, **kwargs)

    return inner


def _is_authorized(request):
    return bool(getattr(request, 'user_id'))
