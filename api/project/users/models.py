from project import database, cache
from project.utils import qb
from .password import check_password

__connection__ = 'default'
__table__ = 'users'

__fields__ = ('id', 'email', 'password', 'type', 'balance')

__cache_key__ = 'users:%s'
__cache_ttl__ = 900  # 15 minutes


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
    q = qb.make('select', __table__)
    qb.set_columns(q, __fields__)
    qb.add_where(q, 'email = {email}', {
        'email': email
    })
    qb.set_limit(q, 1)

    cursor = raw_query(*qb.to_sql(q))

    user = make_user_from_row(cursor.fetchone())

    if user is not None and not check_password(password, user['password']):
        return None

    return user


def get_user_by_id(user_id):
    user_cached = cache.load(__cache_key__ % user_id)
    if user_cached:
        return user_cached

    q = qb.make('select', __table__)
    qb.set_columns(q, __fields__)
    qb.add_where(q, '%(pk)s = {%(pk)s}' % {'pk': __fields__[0]}, {
        __fields__[0]: user_id
    })

    cursor = raw_query(*qb.to_sql(q))

    user = make_user_from_row(cursor.fetchone())

    cache.store(__cache_key__ % user_id, user, __cache_ttl__)

    return user


def increase_user_amount(user_id, amount):
    q = qb.make('update', __table__)
    qb.add_values(q, [
        ('balance', 'balance + {amount}')
    ], {'amount': amount})
    qb.add_where(q, '%s = {pk}' % __fields__[0], {
        'pk': user_id
    })

    raw_query(*qb.to_sql(q), commit=True)

    cache.delete(__cache_key__ % user_id)


def decrease_user_amount(user_id, amount):
    q = qb.make('update', __table__)
    qb.add_values(q, [
        ('balance', 'balance - {amount}')
    ], {'amount': amount})
    qb.add_where(q, '%s = {pk}' % __fields__[0], {
        'pk': user_id
    })

    raw_query(*qb.to_sql(q), commit=True)

    cache.delete(__cache_key__ % user_id)


def create_user(user):
    q = qb.make('insert', __table__)
    qb.set_ignore_mode(q, True)

    qb.add_values(q, [
        (field, '{' + field + '}') for field in __fields__[1:]
    ])

    if user[__fields__[0]]:
        qb.add_values(q, (__fields__[0], '{' + __fields__[0] + '}'))

    qb.add_params(q, user)

    cursor = raw_query(*qb.to_sql(q), commit=True)

    if not cursor.rowcount:
        raise RuntimeError('No users created.')

    user[__fields__[0]] = cursor.lastrowid

    cache.store(__cache_key__ % user['id'], user, __cache_ttl__)

    return user


def raw_query(sql, params=None, commit=False):
    connection = database.get_connection(__connection__)
    return database.execute(connection, sql, params, commit)
