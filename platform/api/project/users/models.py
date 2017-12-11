from project import database
from project.utils import qb
from .password import check_password

user_fields = ('id', 'email', 'password', 'type')


def make_user(**kwargs):
    return {
        field: kwargs.get(field)
        for field in user_fields
    }


def make_user_from_row(row, fields=None):
    fields = fields or user_fields

    if row is not None:
        return make_user(**dict(zip(fields, row)))

    return None


def get_user_by_credentials(email, password):
    conn = database.get_connection()

    q = qb.make('select', 'users')
    qb.set_columns(q, user_fields)
    qb.add_where(q, 'email = :email', {
        'email': email
    })
    qb.set_limit(q, 1)

    result = conn.execute(*qb.to_sql(q))
    user = make_user_from_row(result.fetchone())

    if user is not None and not check_password(password, user['password']):
        return None

    return user


def get_user_by_id(user_id):
    conn = database.get_connection()

    q = qb.make('select', 'users')
    qb.set_columns(q, user_fields)
    qb.add_where(q, 'id = :id', {
        'id': user_id
    })

    result = conn.execute(*qb.to_sql(q))

    return make_user_from_row(result.fetchone())


def update_user(user):
    q = qb.make('update', 'users')
    qb.add_values(q, [
        (field, ':' + field) for field in ('email', 'password', 'type')
    ])
    qb.add_where(q, 'id = :id')
    qb.add_params(q, user)

    conn = database.get_connection()
    result = conn.execute(*qb.to_sql(q))

    if not result.rowcount:
        raise RuntimeError('No users updated.')

    return user


def create_user(user):
    q = qb.make('insert', 'users')

    qb.add_values(q, [
        (field, ':' + field) for field in ('email', 'password', 'type')
    ])

    if user['id']:
        qb.add_values(q, ('id', ':id'))

    qb.add_params(q, user)

    conn = database.get_connection()
    result = conn.execute(*qb.to_sql(q))

    if not result.rowcount:
        raise RuntimeError('No users created.')

    user['id'] = result.lastrowid

    return user
