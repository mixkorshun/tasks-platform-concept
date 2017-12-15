import simplejson
from pymemcache.client import Client


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return simplejson.dumps(value), 2


def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return simplejson.loads(value)

    raise Exception("Unknown serialization format")


def get_connection(host, port):
    client = Client((host, port), serializer=json_serializer,
                    deserializer=json_deserializer)
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
