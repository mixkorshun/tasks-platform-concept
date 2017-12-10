from collections import namedtuple

from project.db import get_db_connection
from .password import check_password

User = namedtuple('User', ('id', 'email', 'password', 'type'))


def get_by_credentials(email, password):
    db = get_db_connection()

    query = 'SELECT %(fields)s FROM users WHERE email = ?' % {
        'fields': ', '.join(User._fields)
    }

    result = db.execute(query, [email])
    row = result.fetchone()

    if row is not None:
        user = User(*row)

        if not check_password(password, user.password):
            user = None
    else:
        user = None

    return user
