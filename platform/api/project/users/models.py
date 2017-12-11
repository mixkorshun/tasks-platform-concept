from project import database, queries
from .password import check_password

user_fields = ('id', 'email', 'password', 'type')


def create_user(**kwargs):
    return {
        field: kwargs.get(field)
        for field in user_fields
    }


def user_from_row(row, fields=None):
    fields = fields or user_fields

    if row is not None:
        return create_user(**dict(zip(fields, row)))

    return None


def get_user_by_credentials(email, password):
    db = database.get_connection()

    row = next(queries.select_objects(
        db, 'users',
        ('email = ?', (email,)),
        fields=user_fields, limit=1
    ), None)

    user = user_from_row(row)
    if row is not None and not check_password(password, user['password']):
        return None

    return user


def get_user_by_id(user_id):
    db = database.get_connection()

    row = queries.get_object_by_pk(
        db, 'users',
        user_id,
        fields=user_fields
    )

    return user_from_row(row)


def save_user(user, force_create=False):
    db = database.get_connection()
    return queries.save_object(
        db, 'users',
        user, force_create=force_create
    )
