import sys

from project import setup


def migrate():
    from project import database
    database.migrate()


def generate_fake_data():
    from project.users.models import make_user, create_user
    from project.users.password import encode_password
    from project.tasks import actions
    from faker import Faker

    employer = create_user(make_user(
        email='employer@platform.loc',
        password=encode_password('qwerty'),
        type='employer',
        balance=100000
    ))

    create_user(make_user(
        email='employee@platform.loc',
        password=encode_password('qwerty'),
        type='employee',
        balance=0
    ))

    fake = Faker()

    for i in range(100):
        actions.add_task(
            name=fake.sentence(),
            price=fake.pydecimal(3, 2, True),
            description=fake.text(),
            author_id=employer['id'],
        )


setup()

migrate()

if '--fake' in sys.argv:
    generate_fake_data()
