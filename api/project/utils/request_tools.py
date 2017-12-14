import json

__all__ = ('get_post_data',)


def get_post_data(request, fields):
    try:
        post_data = json.loads(request.data.decode())
    except (UnicodeEncodeError, json.JSONDecodeError):
        raise ValueError('Invalid POST data.')

    return {field: post_data.get(field, default_value)
            for field, default_value in fields.items()}
