from datetime import datetime

from copy import deepcopy


def get_connection():
    return {}


def add(conn, key, value, ttl=None):
    if key in conn:
        return False

    store(conn, key, value, ttl)

    return True


def load(conn, key, default=None):
    opts = conn.get(key)

    if not opts:
        return default

    value, expire_at = opts

    if expire_at is not None \
            and datetime.utcnow().timestamp() > expire_at:
        del conn[key]
        return default

    return deepcopy(value)


def store(conn, key, value, ttl=None):
    conn[key] = (
        deepcopy(value),
        round(datetime.utcnow().timestamp() + ttl) if ttl is not None else None
    )


def delete(conn, key):
    del conn[key]
