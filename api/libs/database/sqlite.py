import sqlite3

from decimal import Decimal

name = 'sqlite'

sqlite3.register_adapter(Decimal, lambda x: str(x))


def connect(database):
    return sqlite3.connect(database)


def format_param_name(name):
    return ':' + name


DatabaseError = sqlite3.DatabaseError
IntegrityError = sqlite3.IntegrityError
