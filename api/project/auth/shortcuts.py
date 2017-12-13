from functools import wraps

from flask import request
from werkzeug.exceptions import Forbidden

from .utils import is_authorized


def only_authorized(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not is_authorized(request):
            raise Forbidden(
                'Missed or invalid `Authorization` header.'
            )

        return view(*args, **kwargs)

    return inner
