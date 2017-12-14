from pymemcache.client import Client


def get_connection(hosts):
    client = Client(hosts)
    client._connect()
    return client


def add(conn, key, value, ttl=None):
    return conn.add(key, value, ttl)


def load(conn, key, default=None):
    return conn.get(key, default)


def store(conn, key, value, ttl=None):
    return conn.set(key, value, ttl)


def delete(conn, key):
    return conn.delete(key)
