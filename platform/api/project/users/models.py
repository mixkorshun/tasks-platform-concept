from project import database
from project.utils import qb
from .password import check_password

__table__ = 'users'

__fields__ = ('id', 'email', 'password', 'type')


def make_user(**kwargs):
    return {
        field: kwargs.get(field)
        for field in __fields__
    }


def make_user_from_row(row, fields=None):
    fields = fields or __fields__

    if row is not None:
        return make_user(**dict(zip(fields, row)))

    return None


def get_user_by_credentials(email, password):
    conn = database.get_connection()

    q = qb.make('select', __table__)
    qb.set_columns(q, __fields__)
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

    q = qb.make('select', __table__)
    qb.set_columns(q, __fields__)
    qb.add_where(q, '%(pk)s = :%(pk)s' % {'pk': __fields__[0]}, {
        __fields__[0]: user_id
    })

    result = conn.execute(*qb.to_sql(q))

    return make_user_from_row(result.fetchone())


def update_user(user):
    q = qb.make('update', __table__)
    qb.add_values(q, [
        (field, ':' + field) for field in __fields__[1:]
    ])
    qb.add_where(q, '%(pk)s = :%(pk)s' % {'pk': __fields__[0]})
    qb.add_params(q, user)

    conn = database.get_connection()
    result = conn.execute(*qb.to_sql(q))

    if not result.rowcount:
        raise RuntimeError('No users updated.')

    return user


def create_user(user):
    q = qb.make('insert', __table__)

    qb.add_values(q, [
        (field, ':' + field) for field in __fields__[1:]
    ])

    if user[__fields__[0]]:
        qb.add_values(q, (__fields__[0], ':' + __fields__[0]))

    qb.add_params(q, user)

    conn = database.get_connection()
    result = conn.execute(*qb.to_sql(q))

    if not result.rowcount:
        raise RuntimeError('No users created.')

    user[__fields__[0]] = result.lastrowid

    return user
