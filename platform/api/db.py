import importlib
import os
import sqlite3
from urllib.parse import urlparse

import settings


def connect_db(uri):
    uri = urlparse(uri)

    if uri.scheme == 'sqlite':
        return sqlite3.connect(
            uri.path
        )
    else:
        raise NotImplementedError()


db = None


def get_db_connection():
    global db

    if db is None:
        db = connect_db(settings.DATABASE_URL)

    return db


def apply_migrations():
    database = get_db_connection()

    for app_name in settings.INSTALLED_APPS:
        m = importlib.import_module(app_name)

        sql_script = open(os.path.join(
            os.path.dirname(m.__file__),
            'schema', 'schema.sql'
        ), 'r').read()

        database.executescript(sql_script)
