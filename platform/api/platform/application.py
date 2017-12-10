# noinspection PyUnresolvedReferences
import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask  # noqa:

load_dotenv(
    find_dotenv(os.environ.get('ENV_FILE', '.env'))
)


def setup():
    import importlib

    from . import settings

    for app_name in settings.INSTALLED_APPS:
        importlib.import_module(app_name)

    # noinspection PyUnresolvedReferences
    from . import errors


app = Flask(__name__)
