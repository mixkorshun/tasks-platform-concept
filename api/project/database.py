import importlib
import os
import re
from logging import getLogger
from urllib.parse import urlparse

import simplejson

from . import settings

connections = {}

queryLogger = getLogger('platform.database.queries')


def get_connection(name='default'):
    if name in connections:
        conn = connections[name]

        if hasattr(conn, 'ping'):
            conn.ping(True)

        return conn

    database_url = urlparse(settings.DATABASES[name])

    if database_url.scheme == 'sqlite':
        from libs.database import sqlite

        conn = sqlite.connect(
            database_url.netloc + database_url.path
        )
    elif database_url.scheme == 'mysql':
        from libs.database import mysql

        conn = mysql.connect(
            host=database_url.hostname,
            port=database_url.port or 3306,
            user=database_url.username or 'root',
            password=database_url.password or '',
            db=database_url.path.strip('/')
        )
    else:
        raise NotImplementedError(
            'Database `%s` is not supported.' % database_url.scheme
        )

    connections[name] = conn
    return conn


def get_platform_by_connection(connection):
    from libs.database import sqlite
    platforms = {'sqlite3': sqlite}

    try:
        from libs.database import mysql

        # noinspection PyTypeChecker
        platforms.update({'MySQLdb.connections': mysql})
    except ImportError:
        pass

    return platforms.get(type(connection).__module__)


param_regex = re.compile('\{([^\}]+)\}')


def prepare_query(connection, sql):
    params = param_regex.findall(sql)

    platform = get_platform_by_connection(connection)

    # fix insert different insert ignore syntax in SQLite and MySQL
    if platform.name == 'sqlite' and sql.startswith('INSERT IGNORE'):
        sql = sql[:6] + ' OR ' + sql[6:]

    return sql.format(**{
        param: platform.format_param_name(param)
        for param in params
    })


def execute(connection, query, params, commit=False):
    cursor = connection.cursor()

    queryLogger.debug('%s %s' % (query, simplejson.dumps(params)))
    cursor.execute(prepare_query(connection, query), params or {})

    if commit:
        connection.commit()

    return cursor


def migrate():
    for app_name in settings.INSTALLED_APPS:
        app_dir = os.path.dirname(importlib.import_module(app_name).__file__)

        try:
            connection_name = getattr(
                importlib.import_module('%s.models' % app_name),
                '__connection__',
                'default'
            )
        except ImportError:
            connection_name = 'default'

        connection = get_connection(connection_name)

        platform_name = get_platform_by_connection(connection).name

        schema_filename = os.path.join(
            app_dir, 'schema', 'schema.%s.sql' % platform_name
        )

        cursor = connection.cursor()
        if os.path.exists(schema_filename):
            sql_script = open(schema_filename, 'r').read()
            if hasattr(cursor, 'executescript'):
                cursor.executescript(sql_script)
            else:
                cursor.execute(sql_script)

        connection.commit()
