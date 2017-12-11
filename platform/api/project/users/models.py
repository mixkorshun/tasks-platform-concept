from sqlite3 import IntegrityError

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


def save_user(user, force_create=False):
    db = get_db_connection()

    update_fields = ('email', 'password', 'type')

    if user['id'] and not force_create:
        set_statements = ', '.join(
            '%s = :%s' % (x, x) for x in update_fields
        )

        query = 'UPDATE users SET ' + set_statements + ' WHERE id = :id;'
    else:
        if user['id']:
            update_fields += ('id',)

        columns = ', '.join(update_fields)
        values = ', '.join(':' + f for f in update_fields)

        query = 'INSERT INTO users(%(columns)s) VALUES (%(values)s);' % {
            'columns': columns,
            'values': values
        }

    try:
        result = db.execute(query, user)
    except IntegrityError:
        pass

    if result.rowcount == 0:
        raise RuntimeError('User not saved.')

    return result.lastrowid
