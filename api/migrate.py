from project import setup
from project import database

setup()

database.migrate()
