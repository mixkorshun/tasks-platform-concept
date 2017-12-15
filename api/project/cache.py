from urllib.parse import urlparse

from project import settings

_connection = None
_module = None


def _get_connection():
    global _connection, _module

    if not _connection:
        cache_uri = urlparse(getattr(settings, 'CACHE_URL', 'locmem://'))

        if cache_uri.scheme == 'locmem':
            from libs.cache import locmemcache

            _module = locmemcache
            _connection = _module.get_connection()
        elif cache_uri.scheme == 'memcached':
            from libs.cache import memcached

            _module = memcached
            _connection = _module.get_connection(
                cache_uri.hostname, cache_uri.port or 11211
            )
        elif cache_uri.scheme == 'dummy':
            from libs.cache import dummy

            _module = dummy
            _connection = _module.get_connection()
        else:
            raise NotImplementedError()

    return _connection


default_ttl = getattr(settings, 'CACHE_TTL', None)


def add(key, value, ttl=default_ttl):
    conn = _get_connection()

    return _module.add(conn, key, value, ttl)


def load(key, default=None):
    conn = _get_connection()

    return _module.load(conn, key, default)


def store(key, value, ttl=default_ttl):
    conn = _get_connection()

    return _module.store(conn, key, value, ttl)


def delete(key):
    conn = _get_connection()

    return _module.delete(conn, key)
