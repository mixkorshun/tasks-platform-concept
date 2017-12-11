import importlib
import os
import sqlite3
from urllib.parse import urlparse

from . import settings

connection = None


def connect(uri):
    uri = urlparse(uri)

    if uri.scheme == 'sqlite':
        return sqlite3.connect(
            uri.netloc + uri.path
        )
    else:
        raise NotImplementedError()


def get_connection():
    global connection

    if connection is None:
        connection = connect(settings.DATABASE_URL)

    return connection


def migrate():
    conn = get_connection()

    for app_name in settings.INSTALLED_APPS:
        m = importlib.import_module(app_name)

        schema_filename = os.path.join(
            os.path.dirname(m.__file__),
            'schema', 'schema.sql'
        )

        if os.path.exists(schema_filename):
            sql_script = open(schema_filename, 'r').read()
            conn.executescript(sql_script)
