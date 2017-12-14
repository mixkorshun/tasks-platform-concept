from project import database
from project.utils import qb

__table__ = 'tasks'

__fields__ = (
    'id',
    'author_id', 'employee_id',
    'name',
    'status',
    'price',
    'description'
)


def make_task(**kwargs):
    return {
        field: kwargs.get(field) for field in __fields__
    }


def make_task_from_row(row):
    if row is None:
        return None

    return make_task(**dict(zip(__fields__, row)))


def get_task_by_id(task_id):
    q = qb.make('select', __table__)

    qb.set_columns(q, __fields__)
    qb.add_where(q, '%(pk)s = {%(pk)s}' % {'pk': __fields__[0]}, {
        __fields__[0]: task_id
    })

    conn = database.get_connection()

    cursor = conn.cursor()
    sql, params = qb.to_sql(q)
    cursor.execute(database.prepare_query(conn, sql), params)

    return make_task_from_row(cursor.fetchone())


def select_tasks(query):
    if isinstance(query, dict):
        qb.set_table(query, __table__)
        qb.set_columns(query, __fields__)

        query, params = qb.to_sql(query)
    else:
        query, params = query, {}

    conn = database.get_connection()

    cursor = conn.cursor()
    cursor.execute(database.prepare_query(conn, query), params)

    while True:
        row = cursor.fetchone()

        if row is None:
            return

        yield make_task_from_row(row)


def update_tasks(query):
    if isinstance(query, dict):
        qb.set_table(query, __table__)
        qb.set_columns(query, __fields__)

        query, params = qb.to_sql(query)
    else:
        query, params = query, {}

    conn = database.get_connection()

    cursor = conn.cursor()
    cursor.execute(database.prepare_query(conn, query), params)
    conn.commit()

    return cursor.rowcount


def update_task(task):
    q = qb.make('update', __table__)
    qb.add_values(q, [
        (field, '{%s}' % field) for field in __fields__[1:]
    ])
    qb.add_where(q, '%(pk)s = {%(pk)s}' % {
        'pk': __fields__[0]
    })
    qb.add_params(q, task)

    conn = database.get_connection()

    cursor = conn.cursor()
    sql, params = qb.to_sql(q)
    cursor.execute(database.prepare_query(conn, sql), params)
    conn.commit()

    if not cursor.rowcount:
        raise RuntimeError('No tasks updated.')

    return task


def create_task(task):
    q = qb.make('insert', __table__)

    qb.add_values(q, [
        (field, '{%s}' % field) for field in __fields__[1:]
    ])

    if task[__fields__[0]]:
        qb.add_values(q, (__fields__[0], '{' + __fields__[0] + '}'))

    qb.add_params(q, task)

    conn = database.get_connection()

    cursor = conn.cursor()
    sql, params = qb.to_sql(q)
    cursor.execute(database.prepare_query(conn, sql), params)
    conn.commit()

    if not cursor.rowcount:
        raise RuntimeError('No tasks created.')

    task[__fields__[0]] = cursor.lastrowid

    return task
