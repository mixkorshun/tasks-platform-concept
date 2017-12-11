import pytest

from .. import qb


def test_select_query():
    q = qb.make('select', 'tbl1')

    qb.add_where(q, 'id > :last_id', {'last_id': 12})
    qb.add_ordering(q, ('id', 'DESC'))

    sql, params = qb.to_sql(q)

    assert sql == 'SELECT * FROM tbl1 WHERE id > :last_id ORDER BY id DESC'
    assert params == {
        'last_id': 12
    }


def test_insert_query():
    q = qb.make('insert', 'tbl1')

    qb.add_values(q, [
        ('name', ':name'),
        ('age', ':age'),
    ], {'name': 'John', 'age': 24})

    sql, params = qb.to_sql(q)

    assert sql == 'INSERT INTO tbl1 (name, age) ' \
                  'VALUES (:name, :age)'
    assert params == {
        'name': 'John',
        'age': 24,
    }


def test_update_query():
    q = qb.make('update', 'tbl1')

    qb.add_values(q, [
        ('name', ':name'),
        ('age', ':age'),
    ], {'name': 'John', 'age': 24})
    qb.add_where(q, 'id = :id', {'id': 14})

    sql, params = qb.to_sql(q)

    assert sql == 'UPDATE tbl1 SET name = :name, age = :age WHERE id = :id'
    assert params == {
        'id': 14,
        'name': 'John',
        'age': 24,
    }


def test_delete_query():
    q = qb.make('delete', 'tbl1')
    qb.add_where(q, 'id = :id', {'id': 14})

    sql, params = qb.to_sql(q)

    assert sql == 'DELETE FROM tbl1 WHERE id = :id'
    assert params == {
        'id': 14
    }


def test_make_invalid_query():
    with pytest.raises(NotImplementedError):
        qb.make('custom')


def test_to_sql_invalid_query():
    q = qb.make('select')
    q['type'] = 'custom'
    with pytest.raises(NotImplementedError):
        qb.to_sql(q)
