import os

import pytest


def pytest_configure(config):
    os.environ['ENV_FILE'] = '.testenv'

    from project import setup
    setup()

    from project.db import apply_migrations
    apply_migrations()


@pytest.fixture
def app():
    from project import app
    return app
