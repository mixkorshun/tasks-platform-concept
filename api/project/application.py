import os

from flask import Flask


def setup():
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(os.environ.get('ENV_FILE', '.env')))

    from . import settings

    import importlib
    for app_name in settings.INSTALLED_APPS:
        importlib.import_module(app_name)

    # noinspection PyUnresolvedReferences
    from . import errors  # noqa: F401


app = Flask(__name__)


@app.after_request
def after_request(resp):
    from . import settings

    allow_origin = getattr(settings, 'ACCESS_CONTROL_ALLOW_ORIGIN', None)
    if allow_origin:
        resp.headers['Access-Control-Allow-Origin'] = allow_origin
        resp.headers['Access-Control-Allow-Headers'] = 'Authorization'

    return resp
