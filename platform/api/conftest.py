import os

import pytest


def pytest_configure(config):
    os.environ['ENV_FILE'] = '.testenv'

    from project import setup
    setup()

    from project import database
    database.migrate()


def pytest_runtest_setup():
    from project import database

    db = database.get_connection()

    result = db.execute(
        "SELECT `name` FROM sqlite_master WHERE type='table';"
    )

    for name, in result.fetchall():
        db.execute('DELETE FROM %s' % name)


@pytest.fixture
def app():
    from project import app
    return app
