import os

BASE_DIR = os.path.realpath(os.path.dirname(__file__))

SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS = [
    'project.users',
    'project.auth',
]

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'sqlite://db.sqlite3'
)
