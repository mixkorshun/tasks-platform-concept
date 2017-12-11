from project.db import get_db_connection
from .password import check_password

user_fields = ('id', 'email', 'password', 'type')


def create_user(**kwargs):
    user = {
        field: None for field in user_fields
    }

    user.update(kwargs)
    return user


def create_user_from_row(row, fields=None):
    fields = fields or user_fields

    if row is not None:
        return create_user(**dict(zip(fields, row)))

    return None


def get_by_credentials(email, password):
    db = get_db_connection()

    query = 'SELECT %(fields)s FROM users WHERE email = ?' % {
        'fields': ', '.join(user_fields)
    }

    result = db.execute(query, [email])

    user = create_user_from_row(result.fetchone())
    if user is not None and not check_password(password, user['password']):
        return None

    return user


def get_by_id(user_id):
    db = get_db_connection()

    query = 'SELECT %(fields)s FROM users WHERE id = :id' % {
        'fields': ', '.join(user_fields)
    }

    result = db.execute(query, {
        'id': user_id
    })

    return create_user_from_row(result.fetchone())
