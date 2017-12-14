from project.utils import qb


def build_unassigned():
    q = qb.make('select')
    qb.add_ordering(q, ('id', 'DESC'))

    qb.add_where(q, 'employee_id IS NULL')
    qb.add_where(q, 'status = "open"')

    return q


def build_assigned(employee_id):
    q = qb.make('select')
    qb.add_ordering(q, ('id', 'DESC'))

    qb.add_where(q, 'employee_id = {employee_id}', {
        'employee_id': employee_id
    })
    qb.add_where(q, 'status = "open"')

    return q


def build_authored(author_id):
    q = qb.make('select')
    qb.add_ordering(q, ('id', 'DESC'))

    qb.add_where(q, 'author_id = {author_id}', {
        'author_id': author_id
    })
    qb.add_where(q, 'status = "open"')

    return q
