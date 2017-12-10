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
    from . import errors


app = Flask(__name__)
