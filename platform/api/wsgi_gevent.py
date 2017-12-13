from gevent import monkey

monkey.patch_all()

# noinspection PyUnresolvedReferences
from wsgi import app  # noqa:
