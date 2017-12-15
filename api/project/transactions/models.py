from project import database
from project.utils import qb

__table__ = 'transactions'

__fields__ = (
    'id',
    'user_id',
    'task_id',
    'amount'
)


def make_transaction(**kwargs):
    return {
        field: kwargs.get(field) for field in __fields__
    }


def make_transaction_from_row(row):
    if row is None:
        return None

    return make_transaction(**dict(zip(__fields__, row)))


def select_transactions(query):
    if isinstance(query, dict):
        qb.set_table(query, __table__)
        qb.set_columns(query, __fields__)

        query, params = qb.to_sql(query)
    else:
        query, params = query, {}

    cursor = raw_query(query, params)

    while True:
        row = cursor.fetchone()

        if row is None:
            return

        yield make_transaction_from_row(row)


def create_transaction(task):
    q = qb.make('insert', __table__)

    qb.add_values(q, [
        (field, '{%s}' % field) for field in __fields__[1:]
    ])

    if task[__fields__[0]]:
        qb.add_values(q, (__fields__[0], '{' + __fields__[0] + '}'))

    qb.add_params(q, task)

    cursor = raw_query(*qb.to_sql(q), commit=True)

    if not cursor.rowcount:
        raise RuntimeError('No transaction created.')

    task[__fields__[0]] = cursor.lastrowid

    return task


def raw_query(sql, params=None, commit=False):
    connection = database.get_connection()
    return database.execute(connection, sql, params, commit)
