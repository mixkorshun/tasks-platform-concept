import MySQLdb

name = 'mysql'


def connect(host='127.0.0.1', port=3306, user='root', password='', db=None):
    return MySQLdb.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db
    )


def format_param_name(name):
    return '%(' + name + ')s'


DatabaseError = MySQLdb.DatabaseError
IntegrityError = MySQLdb.IntegrityError
