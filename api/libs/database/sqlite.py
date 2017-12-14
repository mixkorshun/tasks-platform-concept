import sqlite3

name = 'sqlite'


def connect(database):
    return sqlite3.connect(database)


def format_param_name(name):
    return ':' + name


DatabaseError = sqlite3.DatabaseError
IntegrityError = sqlite3.IntegrityError
