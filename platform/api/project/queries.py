def select_objects(db, table, where, fields=('*',), limit=None):
    fields = ', '.join(fields)

    q = 'SELECT %(fields)s FROM %(table)s' % {
        'table': table,
        'fields': fields,
    }

    if where:
        q += ' WHERE %s' % where[0]

    if limit:
        q += ' LIMIT %d' % limit

    result = db.execute(q, where[1])

    while True:
        row = result.fetchone()

        if not row:
            break

        yield row


def get_object_by_pk(db, table, pk, fields=('*',), pk_field='id'):
    return next(select_objects(
        db, table,
        ('%s = :pk' % pk_field, {'pk': pk}),
        fields=fields,
        limit=1
    ), None)


def save_object(db, table, obj, pk_field='id', force_create=False):
    update_fields = set(obj.keys())

    if pk_field in update_fields:
        update_fields.remove(pk_field)

    update_fields = tuple(update_fields)

    if obj[pk_field] and not force_create:
        set_statements = ', '.join(
            '%s = :%s' % (x, x) for x in update_fields
        )

        q = 'UPDATE %(table)s SET %(update)s WHERE %(where)s;' % {
            'table': table,
            'update': set_statements,
            'where': 'id = :id'
        }
    else:
        if obj[pk_field]:
            update_fields += (pk_field,)

        columns = ', '.join(update_fields)
        values = ', '.join(':' + f for f in update_fields)

        q = 'INSERT INTO %(table)s(%(columns)s) VALUES (%(values)s);' % {
            'table': table,
            'columns': columns,
            'values': values
        }

    result = db.execute(q, obj)

    if result.rowcount == 0:
        raise RuntimeError('Object not saved.')

    return result.lastrowid
