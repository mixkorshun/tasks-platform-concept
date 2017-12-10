import os

import pytest


def pytest_configure(config):
    os.environ['ENV_FILE'] = '.testenv'

    from platform import setup
    setup()

    from platform.db import apply_migrations
    apply_migrations()


@pytest.fixture
def app():
    from platform import app
    return app
