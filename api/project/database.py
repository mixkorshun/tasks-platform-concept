import importlib
import os
import re
from urllib.parse import urlparse

from . import settings

connection = None


def connect(uri):
    uri = urlparse(uri)

    if uri.scheme == 'sqlite':
        import sqlite3

        return sqlite3.connect(
            uri.netloc + uri.path
        )
    elif uri.scheme == 'mysql':
        import MySQLdb

        return MySQLdb.connect(
            host=uri.hostname,
            port=uri.port or 3306,
            user=uri.username or 'root',
            password=uri.password or '',
            db=uri.path.strip('/')
        )
    else:
        raise NotImplementedError()


def get_connection():
    global connection

    if connection is None:
        connection = connect(settings.DATABASE_URL)

    return connection


def get_platform(conn):
    return {
        'sqlite3': 'sqlite',
        'MySQLdb.connections': 'mysql'
    }.get(type(connection).__module__)


def get_cursor(conn):
    return conn.cursor()


param_regex = re.compile('\{([^\}]+)\}')


def prepare_query(conn, sql):
    params = param_regex.findall(sql)

    platform = get_platform(conn)

    if platform == 'sqlite':
        format_param = lambda x: ':' + x  # noqa: E731
    elif platform == 'mysql':
        format_param = lambda x: '%(' + x + ')s'  # noqa: E731
    else:
        raise NotImplementedError()

    return sql.format(**{
        param: format_param(param) for param in params
    })


def migrate():
    conn = get_connection()
    cursor = conn.cursor()

    for app_name in settings.INSTALLED_APPS:
        m = importlib.import_module(app_name)

        schema_filename = os.path.join(
            os.path.dirname(m.__file__),
            'schema', 'schema.%s.sql' % get_platform(conn)
        )

        if os.path.exists(schema_filename):
            sql_script = open(schema_filename, 'r').read()
            cursor.execute(sql_script)

    conn.commit()
