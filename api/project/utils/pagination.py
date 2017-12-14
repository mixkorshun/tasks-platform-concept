from project.utils import qb


def paginate_by_pk(q, last_pk, limit, pk_field='id'):
    if last_pk:
        qb.add_where(q, '%s < {last_pk}' % pk_field, {
            'last_pk': last_pk
        })

    qb.set_limit(q, limit)
