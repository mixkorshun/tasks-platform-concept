import os

BASE_DIR = os.path.realpath(os.path.dirname(__file__))

SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS = [
    'project.users',
    'project.auth',
    'project.tasks',
    'project.transactions',
]

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'sqlite://db.sqlite3'
)

SYSTEM_COMMISSION = 0.05  # 5%

ACCESS_CONTROL_ALLOW_ORIGIN = os.environ.get('ACCESS_CONTROL_ALLOW_ORIGIN')
