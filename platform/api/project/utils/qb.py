def make(query_type='SELECT', table=None):
    query_type = query_type.upper()

    q = {
        'type': query_type,
        'table': table,
        'where': [],
        'params': {}
    }

    if query_type == 'SELECT':
        q.update({
            'columns': ['*'],
            'ordering': [],
            'limit': None,
            'offset': None,
        })
    elif query_type == 'UPDATE' or query_type == 'INSERT':
        q.update({
            'values': [],
        })
    elif query_type == 'DELETE':
        pass
    else:
        raise NotImplementedError(
            '%s query type is not supported by query builder'
        )

    return q


def set_table(q, table_name):
    q['table'] = table_name


def set_columns(q, columns):
    q['columns'] = columns


def add_where(q, where, params=None):
    if isinstance(where, (list, tuple)):
        q['where'].extend(where)
    else:
        q['where'].append(where)

    if params:
        q['params'].update(params)


def add_ordering(q, ordering):
    q['ordering'].append(ordering)


def set_limit(q, limit, offset=None):
    q['limit'] = limit
    q['offset'] = offset


def add_params(q, params):
    q['params'].update(params)


def add_values(q, values, params=None):
    if isinstance(values, list):
        q['values'].extend(values)
    else:
        q['values'].append(values)

    if params:
        q['params'].update(params)


def __build_cols(cols):
    if not cols:
        cols = ['*']

    return ', '.join(cols)


def __build_insert_cols(values):
    if not values:
        return ''

    return '(' + ', '.join(col for col, val in values) + ')'


def __build_where(where):
    if not where:
        return ''

    return 'WHERE ' + ' AND '.join(where)


def __build_ordering(ordering):
    if not ordering:
        return ''

    def _col(x):
        if not isinstance(x, tuple):
            x = (x, 'ASC')

        return ' '.join(x)

    return 'ORDER BY ' + ', '.join(_col(x) for x in ordering)


def __build_limit(limit, offset):
    part = ''

    if limit:
        part += 'LIMIT ' + str(limit)

    if offset:
        part += ' OFFSET ' + str(offset)

    return part.strip()


def __build_set(values):
    if not values:
        return ''

    return 'SET ' + ', '.join('%s = %s' % (col, val) for col, val in values)


def __build_values(values):
    if not values:
        return ''

    return 'VALUES (' + ', '.join(val for col, val in values) + ')'


def to_sql(q):
    if q['type'] == 'SELECT':
        sql = ' '.join(filter(bool, [
            'SELECT ' + __build_cols(q['columns']) + ' FROM ' + q['table'],
            __build_where(q['where']),
            __build_ordering(q['ordering']),
            __build_limit(q['limit'], q['offset'])
        ]))
    elif q['type'] == 'INSERT':

        sql = ' '.join(filter(bool, [
            'INSERT INTO ' + q['table'],
            __build_insert_cols(q['values']),
            __build_values(q['values']),
            __build_where(q['where'])
        ]))
    elif q['type'] == 'UPDATE':
        sql = ' '.join(filter(bool, [
            'UPDATE ' + q['table'],
            __build_set(q['values']),
            __build_where(q['where'])
        ]))
    elif q['type'] == 'DELETE':
        sql = ' '.join(filter(bool, [
            'DELETE FROM ' + q['table'],
            __build_where(q['where'])
        ]))
    else:
        raise NotImplementedError()

    return sql, q['params']
